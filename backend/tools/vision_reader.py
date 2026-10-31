from pathlib import Path
from PIL import Image
from transformers import pipeline
import gc

MODEL_NAME = "HuggingFaceTB/SmolVLM-256M-Instruct"

vision_model = None


def load_vision_model():
    global vision_model

    if vision_model is None:
        print("\nNEXORA AI: Loading vision model...")

        vision_model = pipeline(
            "image-text-to-text",
            model=MODEL_NAME,
            device=-1
        )

        print("NEXORA AI: Vision model loaded successfully!")

    return vision_model


def analyze_image(image_path, question):
    path = Path(image_path)

    if not path.exists():
        raise FileNotFoundError("Image file not found.")

    allowed_extensions = [
        ".jpg", ".jpeg", ".png", ".webp", ".bmp"
    ]

    if path.suffix.lower() not in allowed_extensions:
        raise ValueError(
            "Supported images: JPG, JPEG, PNG, WEBP and BMP."
        )

    with Image.open(path) as source:
        image = source.convert("RGB")

    model = load_vision_model()

    messages = [
        {
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "image": image
                },
                {
                    "type": "text",
                    "text": question
                }
            ]
        }
    ]

    result = model(
        text=messages,
        max_new_tokens=150
    )

    generated = result[0]["generated_text"]

    if isinstance(generated, list):
        answer = generated[-1]["content"]
    else:
        answer = str(generated)

    del image
    gc.collect()

    return answer