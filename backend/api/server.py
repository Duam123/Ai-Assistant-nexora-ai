
import gc
import shutil
import uuid
from pathlib import Path

from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from starlette.concurrency import run_in_threadpool

from gradio_client import Client

from backend.core.assistant import AURAAssistant
from backend.core.database import get_conversations, get_messages
from backend.tools.web_search import search_web
from backend.tools.web_reader import read_website
from backend.tools.document_reader import read_document
from backend.tools.vision_reader import analyze_image


# --------------------------------------------------
# FASTAPI APP
# --------------------------------------------------

app = FastAPI(
    title="NEXORA AI API",
    description="Local AI Assistant API",
    version="1.1.0"
)


# --------------------------------------------------
# CORS SETTINGS
# --------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


# --------------------------------------------------
# DIRECTORIES
# --------------------------------------------------

assistant = AURAAssistant()

BASE_DIR = Path(__file__).resolve().parents[2]

UPLOAD_DIR = BASE_DIR / "backend" / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

GENERATED_DIR = BASE_DIR / "backend" / "generated"
GENERATED_DIR.mkdir(parents=True, exist_ok=True)

app.mount(
    "/generated",
    StaticFiles(directory=str(GENERATED_DIR)),
    name="generated"
)


# Hugging Face public image-generation Space
HF_SPACE_ID = "mrfakename/Z-Image-Turbo"
hf_client = None


def get_hf_client():
    global hf_client

    if hf_client is None:
        hf_client = Client(HF_SPACE_ID)

    return hf_client


# --------------------------------------------------
# REQUEST MODELS
# --------------------------------------------------

class ChatRequest(BaseModel):
    message: str


class SearchRequest(BaseModel):
    query: str


class URLRequest(BaseModel):
    url: str


class ImageGenerateRequest(BaseModel):
    prompt: str
    height: int = 1024
    width: int = 1024
    num_inference_steps: int = 9
    seed: int = 42
    randomize_seed: bool = True


# --------------------------------------------------
# HEALTH CHECK
# --------------------------------------------------

@app.get("/")
def home():
    return {
        "message": "Welcome to NEXORA AI API"
    }


@app.get("/api/health")
def health():
    return {
        "status": "online",
        "message": "NEXORA AI backend is running"
    }


# --------------------------------------------------
# CHAT API
# --------------------------------------------------

@app.post("/api/chat")
def chat(request: ChatRequest):
    try:
        if not request.message.strip():
            raise HTTPException(
                status_code=400,
                detail="Message cannot be empty"
            )

        answer = assistant.chat(request.message)

        return {
            "answer": answer,
            "conversation_id": getattr(
                assistant, "conversation_id", None
            )
        }

    except HTTPException:
        raise

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=str(error)
        )


# --------------------------------------------------
# NEW CONVERSATION
# --------------------------------------------------

@app.post("/api/conversations/new")
def new_conversation():
    try:
        result = assistant.new_conversation()

        return {
            "message": "New conversation created",
            "conversation": result
        }

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=str(error)
        )


# --------------------------------------------------
# GET ALL CONVERSATIONS
# --------------------------------------------------

@app.get("/api/conversations")
def conversations():
    try:
        return get_conversations()

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=str(error)
        )


# --------------------------------------------------
# OPEN CONVERSATION
# --------------------------------------------------

@app.post("/api/conversations/{conversation_id}/open")
def open_conversation(conversation_id: str):
    try:
        if hasattr(assistant, "load_conversation"):
            assistant.load_conversation(conversation_id)

        messages = get_messages(conversation_id)

        return {
            "conversation_id": conversation_id,
            "messages": messages
        }

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=str(error)
        )


# --------------------------------------------------
# WEB SEARCH
# --------------------------------------------------

@app.post("/api/search")
def web_search(request: SearchRequest):
    try:
        results = search_web(
            request.query,
            max_results=5
        )

        assistant.set_web_search_context(results)

        return {
            "results": results,
            "message": "Search results loaded"
        }

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=str(error)
        )


# --------------------------------------------------
# WEBSITE READER
# --------------------------------------------------

@app.post("/api/url")
def read_url(request: URLRequest):
    try:
        page = read_website(request.url)

        assistant.set_page_context(page)

        return {
            "message": "Website content loaded",
            "page": page
        }

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=str(error)
        )


# --------------------------------------------------
# DOCUMENT UPLOAD
# --------------------------------------------------

@app.post("/api/documents/upload")
async def upload_document(file: UploadFile = File(...)):
    try:
        allowed_extensions = [".pdf", ".txt"]
        extension = Path(file.filename).suffix.lower()

        if extension not in allowed_extensions:
            raise HTTPException(
                status_code=400,
                detail="Only PDF and TXT files are supported"
            )

        content = await file.read()

        if len(content) > 15 * 1024 * 1024:
            raise HTTPException(
                status_code=400,
                detail="File size must be less than 15 MB"
            )

        safe_name = (
            f"{Path(file.filename).stem}_"
            f"{Path(file.filename).suffix}"
        )

        file_path = UPLOAD_DIR / safe_name
        file_path.write_bytes(content)

        document = read_document(str(file_path))

        if not document:
            raise HTTPException(
                status_code=400,
                detail="Could not read this document"
            )

        if getattr(assistant, "documents", None):
            assistant.add_document_context(document)
        else:
            assistant.set_document_context(document)

        return {
            "message": "Document uploaded successfully",
            "filename": file.filename,
            "pages": len(document.get("pages", []))
        }

    except HTTPException:
        raise

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=str(error)
        )


# --------------------------------------------------
# IMAGE ANALYSIS
# --------------------------------------------------

@app.post("/api/images/analyze")
async def image_analysis(
    file: UploadFile = File(...),
    question: str = Form(
        "Describe this image in detail."
    )
):
    try:
        allowed_extensions = [
            ".jpg", ".jpeg", ".png", ".webp", ".bmp"
        ]

        extension = Path(file.filename).suffix.lower()

        if extension not in allowed_extensions:
            raise HTTPException(
                status_code=400,
                detail="Unsupported image format"
            )

        content = await file.read()

        if len(content) > 10 * 1024 * 1024:
            raise HTTPException(
                status_code=400,
                detail="Image size must be less than 10 MB"
            )

        safe_name = f"image_{Path(file.filename).name}"
        file_path = UPLOAD_DIR / safe_name
        file_path.write_bytes(content)

        # Release chat model memory before loading vision model
        assistant.llm.model = None
        gc.collect()

        answer = analyze_image(
            str(file_path),
            question
        )

        return {
            "answer": answer,
            "filename": file.filename
        }

    except HTTPException:
        raise

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=str(error)
        )


# --------------------------------------------------
# AI IMAGE GENERATION - HUGGING FACE
# --------------------------------------------------

@app.post("/api/images/generate")
async def generate_image(request: ImageGenerateRequest):
    try:
        prompt = request.prompt.strip()

        if not prompt:
            raise HTTPException(
                status_code=400,
                detail="Please enter an image prompt."
            )

        if len(prompt) > 2000:
            raise HTTPException(
                status_code=400,
                detail="Prompt must be under 2000 characters."
            )

        if request.height < 512 or request.height > 1024:
            raise HTTPException(
                status_code=400,
                detail="Height must be between 512 and 1024."
            )

        if request.width < 512 or request.width > 1024:
            raise HTTPException(
                status_code=400,
                detail="Width must be between 512 and 1024."
            )

        if request.num_inference_steps < 1 or request.num_inference_steps > 20:
            raise HTTPException(
                status_code=400,
                detail="Steps must be between 1 and 20."
            )

        client = await run_in_threadpool(get_hf_client)

        result = await run_in_threadpool(
            lambda: client.predict(
                prompt,
                request.height,
                request.width,
                request.num_inference_steps,
                request.seed,
                request.randomize_seed,
                api_name="/generate_image"
            )
        )

        if not result or len(result) < 2:
            raise Exception("Hugging Face returned an invalid result.")

        generated_image = result[0]
        seed_used = result[1]

        # Gradio Image output may be a filepath or a dictionary
        if isinstance(generated_image, dict):
            image_path = (
                generated_image.get("path")
                or generated_image.get("name")
            )
        else:
            image_path = generated_image

        if not image_path or not Path(str(image_path)).is_file():
            raise Exception("Generated image file was not found.")

        filename = f"{uuid.uuid4().hex}.png"
        destination = GENERATED_DIR / filename

        shutil.copy2(str(image_path), str(destination))

        return {
            "success": True,
            "message": "Image generated successfully.",
            "image_url": f"/generated/{filename}",
            "seed": seed_used
        }

    except HTTPException:
        raise

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Image generation failed: {str(error)}"
        )
