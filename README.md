# NEXORA AI 🤖

**Your AI-powered assistant for smarter conversations and productivity.**

NEXORA AI is a multi-functional AI assistant built with **React, JavaScript, Python, and FastAPI**. It brings multiple AI-powered features into one user-friendly application, including AI chat, web search, website reading, document upload, image analysis, AI image generation, and voice interaction.

## ✨ Features

- 💬 **AI Chat:** Interact with an AI assistant and get intelligent responses.
- 🗂️ **Conversation History:** Create, view, and reopen previous conversations.
- 🌐 **Web Search:** Search for information online.
- 🔗 **Website Reader:** Read and process website content using a URL.
- 📄 **Document Upload:** Upload PDF and TXT documents.
- 🖼️ **Image Analysis:** Upload images and ask questions about their content.
- 🎨 **AI Image Generation:** Generate images from text prompts.
- 🎤 **Voice Input:** Ask questions using voice.
- 🔊 **Voice Output:** Listen to AI-generated responses.
- 🌙 **Dark & Light Mode:** Switch between interface themes.

## 🛠️ Technologies Used

### Frontend
- React
- JavaScript
- Vite
- Lucide React

### Backend
- Python
- FastAPI
- Uvicorn

### AI Integration
- Hugging Face
- Gradio Client
- Hosted Gradio Space for AI image generation

## 📁 Project Structure

```text
AURA-AI/
│
├── backend/
│   ├── api/
│   │   └── server.py
│   └── generated/
│
├── frontend/
│   └── src/
│       └── App.jsx
│
├── requirements.txt
└── README.md
```

## 🚀 Getting Started

### Prerequisites

- Python
- Node.js and npm
- Git

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

### 2. Open the project folder

```bash
cd AURA-AI
```

### 3. Set up the backend

Create and activate a virtual environment:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

Install Python dependencies:

```bash
pip install -r requirements.txt
```

Start the backend server:

```bash
python -m uvicorn backend.api.server:app --reload
```

Backend URL:

`http://127.0.0.1:8000`

API documentation:

`http://127.0.0.1:8000/docs`

### 4. Set up the frontend

Open another terminal:

```bash
cd frontend
npm install
npm run dev
```

Open the local URL displayed by Vite, usually:

`http://localhost:5173`

## 🔌 Main API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Root endpoint |
| GET | `/api/health` | API health check |
| POST | `/api/chat` | AI conversation |
| POST | `/api/conversations/new` | Create a conversation |
| GET | `/api/conversations` | Get conversation history |
| POST | `/api/conversations/{conversation_id}/open` | Open a conversation |
| POST | `/api/search` | Web search |
| POST | `/api/url` | Website content reader |
| POST | `/api/documents/upload` | Upload documents |
| POST | `/api/images/analyze` | Analyze images |
| POST | `/api/images/generate` | Generate images |

## ⚙️ Important Notes

- AI image generation uses a hosted Hugging Face Gradio Space through `gradio_client`. Its availability and response time depend on the external service.
- Voice features depend on browser and device support.
- Keep API keys and sensitive configuration in environment variables. Never upload `.env` files or private credentials to GitHub.
- Uploaded documents and generated files should be handled carefully and excluded from public commits when they contain user data.

## 🔮 Future Improvements

- Copy and regenerate AI responses.
- Markdown and code syntax highlighting.
- Export conversations as PDF or TXT.
- Improved document question answering with RAG.
- Multiple document management.
- User authentication and database persistence.
- Deployment as a public web application.

## 👩‍💻 Developer

**Dua Mirani**  
Software Engineering Graduate



---

**NEXORA AI — One assistant, multiple possibilities.**
