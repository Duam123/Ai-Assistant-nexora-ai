
import { useEffect, useRef, useState } from "react";
import {
  Sparkles,
  MessageSquare,
  Plus,
  Search,
  Sun,
  Moon,
  Globe,
  Paperclip,
  Send,
  Image as ImageIcon,
  X,
  Menu,
  Bot,
  ExternalLink,
  Mic,
  MicOff,
  Volume2,
  VolumeX,
  WandSparkles,
  Download,
} from "lucide-react";

const API_URL = "http://127.0.0.1:8000";

const styles = `
* { box-sizing: border-box; }
body { margin: 0; font-family: Inter, Arial, sans-serif; }
button, input, textarea { font: inherit; }
button { cursor: pointer; }

.nex-app {
  display: flex; height: 100vh; overflow: hidden;
  background: var(--bg); color: var(--text);
  --bg: #f7f8fc; --panel: #fff; --text: #202333;
  --muted: #85899a; --border: #e8eaf1;
  --accent: #7357e8; --soft: #f0edff; --user: #eeeaff;
}
.nex-app.dark {
  --bg: #11131b; --panel: #1b1e29; --text: #f2f3f8;
  --muted: #a0a4b4; --border: #303342;
  --accent: #a18aff; --soft: #29243e; --user: #29243e;
}
.nex-sidebar {
  width: 270px; min-width: 270px; background: var(--panel);
  border-right: 1px solid var(--border); padding: 20px 14px;
  display: flex; flex-direction: column; gap: 18px;
}
.nex-brand { display: flex; align-items: center; gap: 10px; padding: 4px 8px; }
.nex-brand-icon {
  width: 36px; height: 36px; border-radius: 12px;
  background: var(--accent); color: white; display: grid;
  place-items: center; flex-shrink: 0;
}
.nex-brand strong { font-size: 19px; letter-spacing: .5px; }
.nex-new {
  display: flex; align-items: center; justify-content: center; gap: 9px;
  border: 0; border-radius: 11px; padding: 13px;
  background: var(--accent); color: white; font-weight: 600;
}
.nex-search {
  display: flex; align-items: center; gap: 8px; padding: 10px;
  border: 1px solid var(--border); border-radius: 10px; color: var(--muted);
}
.nex-search input {
  width: 100%; border: 0; outline: 0; background: transparent;
  color: var(--text); min-width: 0;
}
.nex-section-label {
  color: var(--muted); font-size: 11px; font-weight: 700;
  text-transform: uppercase; letter-spacing: 1px; padding: 0 8px;
}
.nex-chat-list { overflow: auto; display: flex; flex-direction: column; gap: 4px; }
.nex-chat-item {
  display: flex; align-items: center; gap: 9px; padding: 10px;
  border: 0; border-radius: 9px; background: transparent;
  color: var(--text); text-align: left; width: 100%; font-size: 13px;
}
.nex-chat-item:hover, .nex-chat-item.active { background: var(--soft); }
.nex-chat-item span { overflow: hidden; text-overflow: ellipsis; white-space: nowrap; flex: 1; }
.nex-sidebar-bottom { margin-top: auto; border-top: 1px solid var(--border); padding-top: 14px; }
.nex-theme {
  display: flex; align-items: center; justify-content: space-between;
  width: 100%; border: 0; background: transparent;
  color: var(--text); padding: 10px; border-radius: 9px;
}
.nex-main { flex: 1; min-width: 0; display: flex; flex-direction: column; }
.nex-header {
  height: 66px; min-height: 66px; display: flex; align-items: center;
  justify-content: space-between; padding: 0 24px;
  border-bottom: 1px solid var(--border); background: var(--panel);
}
.nex-header-left, .nex-header-right { display: flex; align-items: center; gap: 12px; }
.nex-header-title { font-weight: 650; font-size: 15px; }
.nex-icon-btn {
  width: 36px; height: 36px; border: 1px solid var(--border);
  background: var(--panel); color: var(--text); border-radius: 10px;
  display: grid; place-items: center;
}
.nex-content { flex: 1; overflow: auto; padding: 28px 18px 18px; }
.nex-welcome { max-width: 760px; margin: 9vh auto 0; text-align: center; }
.nex-welcome-logo {
  width: 60px; height: 60px; margin: 0 auto 20px;
  display: grid; place-items: center; border-radius: 20px;
  background: var(--soft); color: var(--accent);
}
.nex-welcome h1 { font-size: 32px; margin: 0 0 12px; }
.nex-welcome p { color: var(--muted); line-height: 1.6; }
.nex-suggestions {
  display: grid; grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 12px; margin-top: 32px; text-align: left;
}
.nex-suggestion {
  border: 1px solid var(--border); background: var(--panel);
  color: var(--text); padding: 17px; border-radius: 13px; text-align: left;
}
.nex-suggestion:hover { border-color: var(--accent); }
.nex-suggestion strong { display: block; margin-bottom: 7px; font-size: 14px; }
.nex-suggestion small { color: var(--muted); line-height: 1.5; }
.nex-messages {
  max-width: 850px; margin: 0 auto; display: flex;
  flex-direction: column; gap: 24px;
}
.nex-message { display: flex; align-items: flex-start; gap: 12px; }
.nex-avatar {
  width: 34px; height: 34px; flex-shrink: 0; border-radius: 11px;
  display: grid; place-items: center; background: var(--soft); color: var(--accent);
}
.nex-message-body { min-width: 0; flex: 1; }
.nex-message-name { font-size: 12px; font-weight: 700; margin: 2px 0 8px; }
.nex-message-text {
  font-size: 14px; line-height: 1.75; white-space: pre-wrap; overflow-wrap: anywhere;
}
.nex-user-bubble {
  background: var(--user); padding: 12px 15px;
  border-radius: 4px 13px 13px 13px; display: inline-block; max-width: 100%;
}
.nex-preview {
  display: block; max-width: min(100%, 420px); max-height: 400px;
  object-fit: contain; border-radius: 12px; margin: 10px 0;
  border: 1px solid var(--border);
}
.nex-generated-image {
  display: block; width: 100%; max-width: 512px; height: auto;
  border-radius: 14px; margin-top: 10px; border: 1px solid var(--border);
}
.nex-image-actions { display: flex; gap: 8px; margin-top: 10px; flex-wrap: wrap; }
.nex-image-actions a {
  display: inline-flex; align-items: center; gap: 6px;
  padding: 8px 11px; border-radius: 9px; text-decoration: none;
  color: var(--accent); border: 1px solid var(--border); font-size: 12px;
}
.nex-file-label { font-size: 12px; color: var(--muted); margin-bottom: 8px; }
.nex-results { margin-top: 12px; display: flex; flex-direction: column; gap: 8px; }
.nex-result {
  padding: 11px; border: 1px solid var(--border); border-radius: 10px;
  color: var(--text); text-decoration: none; display: block;
}
.nex-result:hover { border-color: var(--accent); }
.nex-result small { display: block; color: var(--muted); margin-top: 5px; overflow-wrap: anywhere; }
.nex-composer-wrap { padding: 12px 18px 20px; background: var(--bg); }
.nex-composer {
  max-width: 850px; margin: auto; background: var(--panel);
  border: 1px solid var(--border); border-radius: 16px;
  padding: 12px; box-shadow: 0 5px 25px rgba(0,0,0,.04);
}
.nex-composer textarea {
  display: block; width: 100%; resize: vertical; min-height: 55px;
  max-height: 150px; border: 0; outline: 0; background: transparent;
  color: var(--text); padding: 8px; font-size: 14px; line-height: 1.6;
}
.nex-composer-bottom { display: flex; align-items: center; justify-content: space-between; gap: 8px; }
.nex-tools, .nex-send-tools { display: flex; align-items: center; gap: 7px; flex-wrap: wrap; }
.nex-tool {
  display: flex; align-items: center; gap: 6px; padding: 8px 10px;
  border: 1px solid var(--border); border-radius: 9px;
  background: var(--panel); color: var(--muted); font-size: 12px;
}
.nex-tool.active { background: var(--soft); color: var(--accent); border-color: var(--accent); }
.nex-send {
  width: 38px; height: 38px; border: 0; border-radius: 11px;
  display: grid; place-items: center; background: var(--accent); color: white;
}
.nex-send:disabled { opacity: .45; cursor: not-allowed; }
.nex-voice-btn {
  width: 38px; height: 38px; border: 1px solid var(--border);
  border-radius: 11px; display: grid; place-items: center;
  background: var(--panel); color: var(--muted);
}
.nex-voice-btn.active { color: white; background: #e34d65; border-color: #e34d65; }
.nex-voice-btn.speaking { color: var(--accent); background: var(--soft); border-color: var(--accent); }
.nex-voice-btn:disabled { opacity: .4; cursor: not-allowed; }
.nex-voice-note { font-size: 11px; color: var(--muted); padding: 5px 8px; max-width: 850px; margin: 0 auto; }
.nex-status { max-width: 850px; margin: 0 auto 10px; font-size: 12px; color: var(--muted); }
.nex-error { color: #dc5656; }
.nex-loading { color: var(--accent); font-size: 13px; padding: 8px 0; }
.nex-url-panel {
  max-width: 850px; margin: 0 auto 10px; display: flex; gap: 8px;
}
.nex-url-panel input {
  flex: 1; min-width: 0; padding: 11px; border: 1px solid var(--border);
  border-radius: 10px; background: var(--panel); color: var(--text); outline: 0;
}
.nex-url-panel button { padding: 0 14px; background: var(--accent); color: white; border: 0; border-radius: 10px; }
.nex-mobile-menu { display: none; }
.nex-hidden { display: none; }
.nex-mode-note {
  max-width: 850px; margin: 0 auto 8px; color: var(--accent);
  font-size: 12px; display: flex; align-items: center; gap: 6px;
}
@media(max-width: 760px) {
  .nex-sidebar {
    position: absolute; z-index: 5; left: 0; top: 0; bottom: 0;
    box-shadow: 8px 0 30px rgba(0,0,0,.1);
  }
  .nex-sidebar.closed { display: none; }
  .nex-mobile-menu { display: grid; }
  .nex-header { padding: 0 12px; }
  .nex-content { padding: 18px 12px; }
  .nex-suggestions { grid-template-columns: 1fr; }
  .nex-welcome h1 { font-size: 25px; }
  .nex-tools { gap: 4px; }
  .nex-tool { padding: 8px; }
  .nex-tool span { display: none; }
}
@media(max-width: 450px) {
  .nex-composer-bottom { align-items: flex-end; }
  .nex-tools, .nex-send-tools { gap: 4px; }
  .nex-voice-btn, .nex-send { width: 34px; height: 34px; }
}
`;

async function apiRequest(path, options = {}) {
  const response = await fetch(`${API_URL}${path}`, options);
  let data = {};

  try {
    data = await response.json();
  } catch {
    data = {};
  }

  if (!response.ok) {
    throw new Error(
      data.detail || data.message || `Request failed (${response.status})`
    );
  }

  return data;
}

function getError(error) {
  return error?.message || "Something went wrong. Please try again.";
}

function normalizeMessages(items) {
  if (!Array.isArray(items)) return [];

  return items.map((item) => ({
    role: item.role === "user" ? "user" : "assistant",
    content: item.content ?? item.message ?? item.text ?? "",
  }));
}

function getConversationId(data) {
  return (
    data?.conversation_id ??
    data?.conversation?.id ??
    data?.conversation?.conversation_id ??
    data?.id ??
    null
  );
}

function resolveImageUrl(path) {
  if (!path) return "";
  if (path.startsWith("http://") || path.startsWith("https://")) return path;
  return `${API_URL}${path.startsWith("/") ? "" : "/"}${path}`;
}

export default function App() {
  const [dark, setDark] = useState(
    () => localStorage.getItem("nexora-theme") === "dark"
  );

  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [prompt, setPrompt] = useState("");
  const [messages, setMessages] = useState([]);
  const [chats, setChats] = useState([]);
  const [activeChat, setActiveChat] = useState(null);
  const [chatSearch, setChatSearch] = useState("");

  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");
  const [status, setStatus] = useState("");

  const [url, setUrl] = useState("");
  const [showUrl, setShowUrl] = useState(false);

  const [searchQuery, setSearchQuery] = useState("");
  const [searchResults, setSearchResults] = useState([]);
  const [showSearch, setShowSearch] = useState(false);

  // New image generation mode
  const [imageMode, setImageMode] = useState(false);

  const [isListening, setIsListening] = useState(false);
  const [voiceReplies, setVoiceReplies] = useState(true);
  const [speaking, setSpeaking] = useState(false);
  const [voiceSupported, setVoiceSupported] = useState(false);

  const documentInputRef = useRef(null);
  const imageInputRef = useRef(null);
  const bottomRef = useRef(null);
  const promptRef = useRef(null);

  const recognitionRef = useRef(null);
  const voiceTextRef = useRef("");
  const autoSendVoiceRef = useRef(false);
  const sendMessageRef = useRef(null);
  const voiceRepliesRef = useRef(voiceReplies);

  voiceRepliesRef.current = voiceReplies;

  useEffect(() => {
    document.documentElement.dataset.theme = dark ? "dark" : "light";
    localStorage.setItem("nexora-theme", dark ? "dark" : "light");
  }, [dark]);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, isLoading]);

  useEffect(() => {
    loadChats();
  }, []);

  useEffect(() => {
    const SpeechRecognition =
      window.SpeechRecognition || window.webkitSpeechRecognition;

    setVoiceSupported(Boolean(SpeechRecognition && window.speechSynthesis));
    if (!SpeechRecognition) return undefined;

    const recognition = new SpeechRecognition();
    recognition.lang = "en-US";
    recognition.continuous = false;
    recognition.interimResults = false;

    recognition.onstart = () => {
      setIsListening(true);
      setError("");
      setStatus("Listening... Speak your question.");
    };

    recognition.onresult = (event) => {
      const transcript = event.results?.[0]?.[0]?.transcript || "";
      voiceTextRef.current = transcript;
      setPrompt(transcript);
      setStatus(`You said: ${transcript}`);
    };

    recognition.onerror = (event) => {
      setIsListening(false);
      autoSendVoiceRef.current = false;

      if (event.error === "not-allowed") {
        setError("Microphone permission denied. Please allow microphone access.");
      } else if (event.error === "no-speech") {
        setError("No speech detected. Please try again.");
      } else {
        setError(`Voice recognition error: ${event.error}`);
      }
    };

    recognition.onend = () => {
      setIsListening(false);

      if (autoSendVoiceRef.current && voiceTextRef.current.trim()) {
        const spokenText = voiceTextRef.current.trim();
        autoSendVoiceRef.current = false;
        voiceTextRef.current = "";
        setPrompt("");
        sendMessageRef.current?.(spokenText);
      }
    };

    recognitionRef.current = recognition;

    return () => {
      autoSendVoiceRef.current = false;
      try {
        recognition.stop();
      } catch {
        // Already stopped.
      }
      recognitionRef.current = null;
    };
  }, []);

  useEffect(() => {
    return () => window.speechSynthesis?.cancel();
  }, []);

  async function loadChats() {
    try {
      const data = await apiRequest("/api/conversations");
      const list = Array.isArray(data)
        ? data
        : data.conversations || data.results || [];

      setChats(
        list
          .map((item) => ({
            id: item.id ?? item.conversation_id,
            title: item.title ?? item.name ?? "New conversation",
          }))
          .filter((item) => item.id)
      );
    } catch (err) {
      console.error("Conversation history:", err);
    }
  }

  async function newChat() {
    stopSpeaking();
    stopListening();
    setError("");
    setStatus("");
    setSearchResults([]);
    setShowSearch(false);
    setShowUrl(false);
    setImageMode(false);
    setMessages([]);
    setPrompt("");

    try {
      const data = await apiRequest("/api/conversations/new", {
        method: "POST",
      });
      setActiveChat(getConversationId(data));
      await loadChats();
    } catch (err) {
      setActiveChat(null);
      setError("New chat could not be created: " + getError(err));
    }

    promptRef.current?.focus();
  }

  async function openChat(id) {
    if (!id || isLoading) return;

    stopSpeaking();
    stopListening();
    setIsLoading(true);
    setError("");
    setStatus("");
    setSearchResults([]);
    setImageMode(false);

    try {
      const data = await apiRequest(
        `/api/conversations/${encodeURIComponent(id)}/open`,
        { method: "POST" }
      );

      setActiveChat(id);
      setMessages(normalizeMessages(data.messages));
      setShowSearch(false);
      setShowUrl(false);
    } catch (err) {
      setError("Could not open conversation: " + getError(err));
    } finally {
      setIsLoading(false);
    }
  }

  async function sendMessage(textOverride) {
    const text = (textOverride ?? prompt).trim();
    if (!text || isLoading) return;

    stopSpeaking();
    setError("");
    setStatus("");
    setSearchResults([]);

    setMessages((previous) => [
      ...previous,
      { role: "user", content: text },
    ]);

    setPrompt("");
    setIsLoading(true);

    try {
      const data = await apiRequest("/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          message: text,
          conversation_id: activeChat,
        }),
      });

      const answer = data.answer || "No response received.";

      setMessages((previous) => [
        ...previous,
        { role: "assistant", content: answer },
      ]);

      if (voiceRepliesRef.current) speakAnswer(answer);

      const id = data.conversation_id || activeChat;
      if (id) setActiveChat(id);

      await loadChats();
    } catch (err) {
      setError(getError(err));
      setMessages((previous) => [
        ...previous,
        {
          role: "assistant",
          content: "I couldn't complete that request. Please check that the backend is running and try again.",
        },
      ]);
    } finally {
      setIsLoading(false);
    }
  }

  // Generate an image from the user's text prompt
  async function generateImage(textOverride) {
    const text = (textOverride ?? prompt).trim();

    if (!text || isLoading) return;

    stopSpeaking();
    setError("");
    setStatus("Sending your prompt to the image generation model...");

    setMessages((previous) => [
      ...previous,
      { role: "user", content: text, type: "image-prompt" },
    ]);

    setPrompt("");
    setIsLoading(true);

    try {
      const data = await apiRequest("/api/images/generate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          prompt: text,
          height: 1024,
          width: 1024,
          num_inference_steps: 9,
          seed: 42,
          randomize_seed: true,
        }),
      });

      if (!data.image_url) {
        throw new Error("The image service did not return an image URL.");
      }

      const imageUrl = resolveImageUrl(data.image_url);

      setMessages((previous) => [
        ...previous,
        {
          role: "assistant",
          content: data.message || "Here is your generated image.",
          imageUrl,
          seed: data.seed,
          type: "generated-image",
        },
      ]);

      setStatus("Your image has been generated successfully.");
      await loadChats();
    } catch (err) {
      const message = getError(err);
      setError(message);
      setStatus("");

      setMessages((previous) => [
        ...previous,
        {
          role: "assistant",
          content: `Image generation failed: ${message}`,
        },
      ]);
    } finally {
      setIsLoading(false);
    }
  }

  sendMessageRef.current = (text) => {
    if (imageMode) {
      generateImage(text);
    } else {
      sendMessage(text);
    }
  };

  function startListening() {
    if (!recognitionRef.current) {
      setError("Speech recognition is not supported. Please use Chrome or Edge.");
      return;
    }

    if (isLoading || isListening) return;

    stopSpeaking();
    voiceTextRef.current = "";
    autoSendVoiceRef.current = true;

    try {
      recognitionRef.current.start();
    } catch {
      autoSendVoiceRef.current = false;
      setError("Microphone is already active. Please try again.");
    }
  }

  function stopListening() {
    autoSendVoiceRef.current = false;
    voiceTextRef.current = "";

    try {
      recognitionRef.current?.stop();
    } catch {
      // Already stopped.
    }

    setIsListening(false);
  }

  function speakAnswer(text) {
    if (!window.speechSynthesis) {
      setError("Text-to-speech is not supported in this browser.");
      return;
    }

    window.speechSynthesis.cancel();

    const cleanText = String(text)
      .replace(/```[\s\S]*?```/g, " Code block omitted. ")
      .replace(/https?:\/\/\S+/g, "link")
      .replace(/[*_#\`]/g, "")
      .replace(/\s+/g, " ")
      .trim();

    if (!cleanText) return;

    const utterance = new SpeechSynthesisUtterance(cleanText);
    utterance.lang = "en-US";
    utterance.rate = 1;
    utterance.pitch = 1;
    utterance.onstart = () => setSpeaking(true);
    utterance.onend = () => setSpeaking(false);
    utterance.onerror = () => setSpeaking(false);

    window.speechSynthesis.speak(utterance);
  }

  function stopSpeaking() {
    window.speechSynthesis?.cancel();
    setSpeaking(false);
  }

  async function uploadDocuments(event) {
    const files = Array.from(event.target.files || []);
    event.target.value = "";
    if (!files.length) return;

    for (const file of files) {
      setError("");
      setStatus(`Uploading ${file.name}...`);
      setIsLoading(true);

      try {
        const formData = new FormData();
        formData.append("file", file);

        const data = await apiRequest("/api/documents/upload", {
          method: "POST",
          body: formData,
        });

        setMessages((previous) => [
          ...previous,
          {
            role: "assistant",
            content: `📄 ${data.message || "Document uploaded successfully"}: ${data.filename || file.name}. You can now ask questions about this document.`,
          },
        ]);

        setStatus(`${file.name} uploaded successfully.`);
      } catch (err) {
        setError(`${file.name}: ${getError(err)}`);
      } finally {
        setIsLoading(false);
      }
    }
  }

  // Existing image upload and analysis feature
  async function uploadImage(event) {
    const file = event.target.files?.[0];
    event.target.value = "";
    if (!file) return;

    const previewUrl = URL.createObjectURL(file);
    const question = prompt.trim() || "Describe this image in detail.";

    setPrompt("");
    setError("");
    setStatus("");

    setMessages((previous) => [
      ...previous,
      {
        role: "user",
        content: question,
        image: previewUrl,
        filename: file.name,
      },
    ]);

    setIsLoading(true);

    try {
      const formData = new FormData();
      formData.append("file", file);
      formData.append("question", question);

      const data = await apiRequest("/api/images/analyze", {
        method: "POST",
        body: formData,
      });

      const answer = data.answer || "I couldn't analyze this image.";

      setMessages((previous) => [
        ...previous,
        { role: "assistant", content: answer },
      ]);

      if (voiceRepliesRef.current) speakAnswer(answer);
      setStatus("Image analysis completed.");
    } catch (err) {
      setError(getError(err));
    } finally {
      setIsLoading(false);
    }
  }

  async function runSearch() {
    const query = searchQuery.trim();
    if (!query || isLoading) return;

    setError("");
    setStatus("Searching the web...");
    setIsLoading(true);

    try {
      const data = await apiRequest("/api/search", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query }),
      });

      const results = Array.isArray(data.results)
        ? data.results
        : Array.isArray(data.results?.results)
          ? data.results.results
          : [];

      setSearchResults(results);

      setMessages((previous) => [
        ...previous,
        {
          role: "assistant",
          content: data.message || `Web search completed for: ${query}. You can now ask me about these search results.`,
        },
      ]);

      setStatus(
        results.length
          ? `${results.length} search results loaded. Ask me about them below.`
          : "Search completed. Ask me about the results in the chat."
      );

      setShowSearch(true);
      setShowUrl(false);
    } catch (err) {
      setError(getError(err));
      setStatus("");
    } finally {
      setIsLoading(false);
    }
  }

  async function readUrl() {
    const target = url.trim();
    if (!target || isLoading) return;

    setError("");
    setStatus("Reading website...");
    setIsLoading(true);

    try {
      const data = await apiRequest("/api/url", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ url: target }),
      });

      const page = data.page || {};

      setMessages((previous) => [
        ...previous,
        {
          role: "assistant",
          content: `${data.message || "Website content loaded"}${page.title ? `: ${page.title}` : ""}. You can now ask me questions about this website.`,
        },
      ]);

      setStatus("Website content loaded. Ask a question about it in the chat.");
      setUrl("");
      setShowUrl(false);
      setShowSearch(false);
    } catch (err) {
      setError(getError(err));
      setStatus("");
    } finally {
      setIsLoading(false);
    }
  }

  function handleSubmit() {
    if (imageMode) {
      generateImage();
    } else {
      sendMessage();
    }
  }

  const filteredChats = chats.filter((chat) =>
    (chat.title || "").toLowerCase().includes(chatSearch.toLowerCase())
  );

  return (
    <>
      <style>{styles}</style>

      <div className={`nex-app ${dark ? "dark" : ""}`}>
        <aside className={`nex-sidebar ${sidebarOpen ? "" : "closed"}`}>
          <div className="nex-brand">
            <div className="nex-brand-icon"><Sparkles size={21} /></div>
            <strong>NEXORA AI</strong>
          </div>

          <button className="nex-new" onClick={newChat}>
            <Plus size={18} /> New Chat
          </button>

          <div className="nex-search">
            <Search size={16} />
            <input
              placeholder="Search conversations..."
              value={chatSearch}
              onChange={(e) => setChatSearch(e.target.value)}
            />
          </div>

          <div className="nex-section-label">Your conversations</div>

          <div className="nex-chat-list">
            {filteredChats.map((chat) => (
              <button
                key={chat.id}
                className={`nex-chat-item ${activeChat === chat.id ? "active" : ""}`}
                onClick={() => openChat(chat.id)}
              >
                <MessageSquare size={16} />
                <span>{chat.title}</span>
              </button>
            ))}

            {!filteredChats.length && (
              <div style={{ color: "var(--muted)", fontSize: 12, padding: 10 }}>
                No conversations found.
              </div>
            )}
          </div>

          <div className="nex-sidebar-bottom">
            <button className="nex-theme" onClick={() => setDark((p) => !p)}>
              <span style={{ display: "flex", gap: 9, alignItems: "center" }}>
                {dark ? <Sun size={17} /> : <Moon size={17} />}
                {dark ? "Light mode" : "Dark mode"}
              </span>
            </button>

            <div style={{ color: "var(--muted)", fontSize: 11, padding: 10 }}>
              NEXORA AI · Local Assistant
            </div>
          </div>
        </aside>

        <main className="nex-main">
          <header className="nex-header">
            <div className="nex-header-left">
              <button
                className="nex-icon-btn nex-mobile-menu"
                onClick={() => setSidebarOpen((p) => !p)}
              >
                <Menu size={18} />
              </button>
              <div className="nex-header-title">NEXORA AI Assistant</div>
            </div>

            <div className="nex-header-right">
              <span style={{ fontSize: 11, color: "var(--muted)" }}>Local AI</span>
              <div className="nex-brand-icon" style={{ width: 32, height: 32 }}>
                <Bot size={18} />
              </div>
            </div>
          </header>

          <section className="nex-content">
            {messages.length === 0 ? (
              <div className="nex-welcome">
                <div className="nex-welcome-logo"><Sparkles size={30} /></div>
                <h1>Welcome to NEXORA AI</h1>
                <p>
                  Your personal AI assistant. Chat, generate images,
                  understand pictures, explore websites, search the web
                  and ask questions about your documents.
                </p>

                <div className="nex-suggestions">
                  <button
                    className="nex-suggestion"
                    onClick={() => sendMessage("Explain artificial intelligence in simple words.")}
                  >
                    <strong>✨ Learn something</strong>
                    <small>Explain a topic in simple words</small>
                  </button>

                  <button
                    className="nex-suggestion"
                    onClick={() => {
                      setShowSearch(true);
                      setShowUrl(false);
                      setImageMode(false);
                    }}
                  >
                    <strong>🌐 Search the web</strong>
                    <small>Find information from the internet</small>
                  </button>

                  <button
                    className="nex-suggestion"
                    onClick={() => documentInputRef.current?.click()}
                  >
                    <strong>📄 Ask about a document</strong>
                    <small>Upload a PDF or TXT file</small>
                  </button>

                  <button
                    className="nex-suggestion"
                    onClick={() => {
                      setImageMode(true);
                      setShowSearch(false);
                      setShowUrl(false);
                      promptRef.current?.focus();
                    }}
                  >
                    <strong>🎨 Generate an image</strong>
                    <small>Create a new image from a text prompt</small>
                  </button>

                  <button
                    className="nex-suggestion"
                    onClick={() => imageInputRef.current?.click()}
                  >
                    <strong>🖼️ Understand an image</strong>
                    <small>Upload an image and ask a question</small>
                  </button>
                </div>
              </div>
            ) : (
              <div className="nex-messages">
                {messages.map((item, index) => (
                  <div className={`nex-message ${item.role}`} key={index}>
                    <div className="nex-avatar">
                      {item.role === "user" ? <span>U</span> : <Sparkles size={18} />}
                    </div>

                    <div className="nex-message-body">
                      <div
                        style={{
                          display: "flex",
                          alignItems: "center",
                          justifyContent: "space-between",
                          marginBottom: 8,
                        }}
                      >
                        <div className="nex-message-name" style={{ margin: 0 }}>
                          {item.role === "user" ? "You" : "NEXORA AI"}
                        </div>

                        {item.role === "assistant" && item.content && (
                          <button
                            className="nex-voice-btn"
                            title="Listen to this answer"
                            onClick={() => speakAnswer(item.content)}
                          >
                            <Volume2 size={17} />
                          </button>
                        )}
                      </div>

                      {item.image && (
                        <>
                          <img
                            className="nex-preview"
                            src={item.image}
                            alt={item.filename || "Uploaded image"}
                          />
                          <div className="nex-file-label">
                            <ImageIcon size={12} style={{ verticalAlign: "middle" }} />
                            {" "}{item.filename}
                          </div>
                        </>
                      )}

                      <div className={item.role === "user" ? "nex-user-bubble nex-message-text" : "nex-message-text"}>
                        {item.content}
                      </div>

                      {item.imageUrl && (
                        <div>
                          <a href={item.imageUrl} target="_blank" rel="noreferrer">
                            <img
                              className="nex-generated-image"
                              src={item.imageUrl}
                              alt="AI generated image"
                              loading="lazy"
                            />
                          </a>

                          <div className="nex-image-actions">
                            <a href={item.imageUrl} target="_blank" rel="noreferrer">
                              <ExternalLink size={14} /> Open image
                            </a>
                            <a href={item.imageUrl} download="nexora-generated-image.png">
                              <Download size={14} /> Download image
                            </a>
                          </div>

                          {item.seed !== undefined && item.seed !== null && (
                            <div className="nex-file-label" style={{ marginTop: 8 }}>
                              Seed: {item.seed}
                            </div>
                          )}
                        </div>
                      )}
                    </div>
                  </div>
                ))}

                {showSearch && searchResults.length > 0 && (
                  <div className="nex-message">
                    <div className="nex-avatar"><Globe size={18} /></div>
                    <div className="nex-message-body">
                      <div className="nex-message-name">Web search results</div>
                      <div className="nex-results">
                        {searchResults.map((result, index) => (
                          <a
                            className="nex-result"
                            key={index}
                            href={result.url || "#"}
                            target="_blank"
                            rel="noreferrer"
                          >
                            <strong>{result.title || result.name || "Search result"}</strong>
                            <small>{result.url || ""}</small>
                            {result.snippet && <small>{result.snippet}</small>}
                          </a>
                        ))}
                      </div>
                    </div>
                  </div>
                )}

                {isLoading && (
                  <div className="nex-loading">
                    {imageMode
                      ? "🎨 NEXORA AI is generating your image. This may take a little while..."
                      : "NEXORA AI is working..."}
                  </div>
                )}

                <div ref={bottomRef} />
              </div>
            )}
          </section>

          <div className="nex-composer-wrap">
            {error && <div className="nex-status nex-error">{error}</div>}
            {status && <div className="nex-status">{status}</div>}

            {isListening && (
              <div className="nex-voice-note">🎙️ Listening... Speak your question.</div>
            )}

            {!voiceSupported && (
              <div className="nex-voice-note">
                Voice input requires a supported browser such as Chrome or Edge.
              </div>
            )}

            {imageMode && (
              <div className="nex-mode-note">
                <WandSparkles size={15} />
                Image generation mode — describe the image you want to create.
                <button
                  onClick={() => setImageMode(false)}
                  style={{
                    border: 0,
                    background: "transparent",
                    color: "var(--accent)",
                    marginLeft: "auto",
                    display: "flex",
                    alignItems: "center",
                    gap: 4,
                  }}
                >
                  <X size={14} /> Exit
                </button>
              </div>
            )}

            {showSearch && (
              <div className="nex-url-panel">
                <input
                  placeholder="What do you want to search on the web?"
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  onKeyDown={(e) => { if (e.key === "Enter") runSearch(); }}
                />
                <button onClick={runSearch} disabled={isLoading}>Search</button>
                <button
                  onClick={() => setShowSearch(false)}
                  style={{ background: "var(--panel)", color: "var(--text)", border: "1px solid var(--border)" }}
                >
                  <X size={16} />
                </button>
              </div>
            )}

            {showUrl && (
              <div className="nex-url-panel">
                <input
                  placeholder="Paste a website URL (https://...)"
                  value={url}
                  onChange={(e) => setUrl(e.target.value)}
                  onKeyDown={(e) => { if (e.key === "Enter") readUrl(); }}
                />
                <button onClick={readUrl} disabled={isLoading}>Read Website</button>
                <button
                  onClick={() => setShowUrl(false)}
                  style={{ background: "var(--panel)", color: "var(--text)", border: "1px solid var(--border)" }}
                >
                  <X size={16} />
                </button>
              </div>
            )}

            <div className="nex-composer">
              <textarea
                ref={promptRef}
                placeholder={
                  imageMode
                    ? "Describe the image you want NEXORA AI to generate..."
                    : "Message NEXORA AI..."
                }
                value={prompt}
                onChange={(e) => setPrompt(e.target.value)}
                onKeyDown={(e) => {
                  if (e.key === "Enter" && !e.shiftKey) {
                    e.preventDefault();
                    handleSubmit();
                  }
                }}
              />

              <div className="nex-composer-bottom">
                <div className="nex-tools">
                  <button
                    className="nex-tool"
                    title="Upload PDF or TXT"
                    onClick={() => documentInputRef.current?.click()}
                  >
                    <Paperclip size={16} /><span>Attach</span>
                  </button>

                  <button
                    className="nex-tool"
                    title="Upload image for analysis"
                    onClick={() => imageInputRef.current?.click()}
                  >
                    <ImageIcon size={16} /><span>Analyze</span>
                  </button>

                  <button
                    className={`nex-tool ${imageMode ? "active" : ""}`}
                    title="Generate image from prompt"
                    onClick={() => {
                      setImageMode((previous) => !previous);
                      setShowSearch(false);
                      setShowUrl(false);
                      promptRef.current?.focus();
                    }}
                  >
                    <WandSparkles size={16} /><span>Generate</span>
                  </button>

                  <button
                    className={`nex-tool ${showSearch ? "active" : ""}`}
                    title="Web search"
                    onClick={() => {
                      setShowSearch((previous) => !previous);
                      setShowUrl(false);
                      setImageMode(false);
                    }}
                  >
                    <Globe size={16} /><span>Search</span>
                  </button>

                  <button
                    className={`nex-tool ${showUrl ? "active" : ""}`}
                    title="Read a website"
                    onClick={() => {
                      setShowUrl((previous) => !previous);
                      setShowSearch(false);
                      setImageMode(false);
                    }}
                  >
                    <ExternalLink size={15} /><span>Website</span>
                  </button>
                </div>

                <div className="nex-send-tools">
                  <button
                    className={`nex-voice-btn ${isListening ? "active" : ""}`}
                    onClick={isListening ? stopListening : startListening}
                    disabled={!voiceSupported || isLoading}
                    title={isListening ? "Stop listening" : "Speak your question"}
                  >
                    {isListening ? <MicOff size={18} /> : <Mic size={18} />}
                  </button>

                  <button
                    className={`nex-voice-btn ${voiceReplies ? "speaking" : ""}`}
                    onClick={() => {
                      if (voiceReplies) stopSpeaking();
                      setVoiceReplies((previous) => !previous);
                    }}
                    title={voiceReplies ? "Turn voice replies off" : "Turn voice replies on"}
                  >
                    {voiceReplies ? <Volume2 size={18} /> : <VolumeX size={18} />}
                  </button>

                  {speaking && (
                    <button className="nex-voice-btn" onClick={stopSpeaking} title="Stop AI voice">
                      <X size={18} />
                    </button>
                  )}

                  <button
                    className="nex-send"
                    onClick={handleSubmit}
                    disabled={!prompt.trim() || isLoading}
                    title={imageMode ? "Generate image" : "Send message"}
                  >
                    {imageMode ? <WandSparkles size={18} /> : <Send size={17} />}
                  </button>
                </div>
              </div>
            </div>

            <div
              style={{
                maxWidth: 850,
                margin: "8px auto 0",
                textAlign: "center",
                color: "var(--muted)",
                fontSize: 10,
              }}
            >
              NEXORA AI can make mistakes. Verify important information.
            </div>
          </div>

          <input
            ref={documentInputRef}
            className="nex-hidden"
            type="file"
            accept=".pdf,.txt"
            multiple
            onChange={uploadDocuments}
          />

          <input
            ref={imageInputRef}
            className="nex-hidden"
            type="file"
            accept=".jpg,.jpeg,.png,.webp,.bmp"
            onChange={uploadImage}
          />
        </main>
      </div>
    </>
  );
}
