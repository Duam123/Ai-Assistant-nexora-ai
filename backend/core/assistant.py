
from backend.core.llm import LocalLLM

from backend.core.database import (
    create_conversation,
    save_message,
    get_messages,
    update_conversation_title
)

from backend.rag.document_rag import DocumentRAG


SYSTEM_PROMPT = """
You are NEXORA AI, an intelligent personal AI assistant.

You are also a programming and software engineering assistant.

YOUR CAPABILITIES:

1. General knowledge and research.
2. Programming and software development.
3. Python, JavaScript, Java, C++, HTML, CSS and SQL.
4. Artificial intelligence and machine learning.
5. Debugging and troubleshooting.
6. Code explanation and documentation.
7. Education and technical learning.
8. Writing and problem solving.
9. Website and document understanding.

PROGRAMMING INSTRUCTIONS:

- Generate complete and readable code when requested.
- Use correct syntax and proper indentation.
- Explain important parts of the code.
- When debugging, identify the likely cause of the error.
- Give step-by-step solutions.
- Show corrected code when possible.
- Never claim code was executed or tested unless it actually was.
- If required information is missing, ask the user.
- Do not invent files, functions or project structures.

RESPONSE FORMATTING:

- Use Markdown headings where useful.
- Put programming code inside language-specific code blocks.
- Use bullet points for explanations.
- Keep answers clear and beginner-friendly.
- Explain technical terms in simple language when appropriate.

DOCUMENT INSTRUCTIONS:

- Use provided document context.
- Cite filename and page number when available.
- Never invent page numbers or document information.

WEB INSTRUCTIONS:

- Use provided website or web research context.
- Cite source titles and exact URLs when available.
- Never invent sources or links.

GENERAL INSTRUCTIONS:

- Be helpful, accurate and honest.
- If uncertain, say so.
- Do not claim to have performed actions you have not performed.
"""


class AURAAssistant:

    def __init__(self):

        self.llm = LocalLLM()

        self.conversation_id = create_conversation()

        self.history = [
            {"role": "system", "content": SYSTEM_PROMPT}
        ]

        self.page_context = None
        self.web_search_context = None
        self.documents = []
        self.document_rag = None

    def new_conversation(self):

        self.conversation_id = create_conversation()

        self.reset_chat()

        print(
            "\nNEXORA AI: New conversation created!",
            self.conversation_id,
            "\n"
        )

        return {
            "conversation_id": self.conversation_id
        }

    def load_conversation(self, conversation_id):

        saved_messages = get_messages(conversation_id)

        self.conversation_id = conversation_id

        self.history = [
            {"role": "system", "content": SYSTEM_PROMPT}
        ]

        for message in saved_messages:

            self.history.append({
                "role": message["role"],
                "content": message["content"]
            })

        self.page_context = None
        self.web_search_context = None
        self.documents = []
        self.document_rag = None

    def set_page_context(self, page):

        self.page_context = page
        self.web_search_context = None
        self.documents = []
        self.document_rag = None

        self.reset_chat()

    def set_web_search_context(self, results):

        self.web_search_context = results
        self.page_context = None
        self.documents = []
        self.document_rag = None

        self.reset_chat()

    def set_document_context(self, document):

        self.documents = [document]

        self.page_context = None
        self.web_search_context = None

        self.rebuild_document_rag()
        self.reset_chat()

    def add_document_context(self, document):

        self.documents.append(document)

        self.page_context = None
        self.web_search_context = None

        self.rebuild_document_rag()
        self.reset_chat()

    def rebuild_document_rag(self):

        self.document_rag = DocumentRAG(self.documents)

    def chat(self, user_message):

        self.history.append({
            "role": "user",
            "content": user_message
        })

        messages = self.history.copy()

        if self.page_context:

            context = (
                "Website: " + self.page_context["url"] +
                "\nTitle: " + self.page_context["title"] +
                "\nWebsite content:\n" +
                self.page_context["content"]
            )

            messages.insert(1, {
                "role": "system",
                "content": context
            })

        elif self.web_search_context:

            passages = []

            for index, page in enumerate(
                self.web_search_context["pages"],
                start=1
            ):

                passages.append(
                    f"Source {index}\n"
                    f"Title: {page['title']}\n"
                    f"URL: {page['url']}\n"
                    f"Content:\n{page['content']}"
                )

            context = (
                "Research query: "
                + self.web_search_context["query"]
                + "\nUse these sources to answer. Cite the title "
                "and exact URL. Do not invent facts or sources.\n\n"
                + "\n\n".join(passages)
            )

            messages.insert(1, {
                "role": "system",
                "content": context
            })

        elif self.document_rag:

            results = self.document_rag.search(
                user_message,
                top_k=4
            )

            passages = []

            for index, item in enumerate(results, start=1):

                passages.append(
                    f"Passage {index}\n"
                    f"Source: {item['filename']}, "
                    f"Page: {item['page']}\n"
                    f"{item['text']}"
                )

            context = (
                "Answer using these retrieved document passages. "
                "Cite filename and page number. "
                "Do not invent sources.\n\n"
                + "\n\n".join(passages)
            )

            messages.insert(1, {
                "role": "system",
                "content": context
            })

        try:

            answer = self.llm.generate(messages)

            self.history.append({
                "role": "assistant",
                "content": answer
            })

            save_message(
                self.conversation_id,
                "user",
                user_message
            )

            save_message(
                self.conversation_id,
                "assistant",
                answer
            )

            saved_messages = get_messages(
                self.conversation_id
            )

            if len(saved_messages) == 2:

                title = user_message[:50]

                update_conversation_title(
                    self.conversation_id,
                    title
                )

            if len(self.history) > 9:

                self.history = (
                    [self.history[0]] + self.history[-8:]
                )

            return answer

        except Exception:

            self.history.pop()

            raise

    def reset_chat(self):

        self.history = [
            {"role": "system", "content": SYSTEM_PROMPT}
        ]
