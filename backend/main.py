
import gc

from backend.core.assistant import AURAAssistant
from backend.core.database import get_conversations
from backend.tools.web_reader import read_website
from backend.tools.web_search import search_web
from backend.tools.document_reader import read_document
from backend.tools.vision_reader import analyze_image


def parse_image_command(command):
    argument = command[6:].strip()

    if not argument:
        raise ValueError("Please provide an image path.")

    if argument.startswith('"') or argument.startswith("'"):
        quote = argument[0]
        end = argument.find(quote, 1)

        if end == -1:
            raise ValueError("Please close the quotation marks.")

        image_path = argument[1:end]
        question = argument[end + 1:].strip()

    else:
        parts = argument.split(maxsplit=1)
        image_path = parts[0]
        question = parts[1] if len(parts) > 1 else ""

    if not question:
        question = "Describe this image in detail."

    return image_path, question


def parse_file_path(command, prefix):
    argument = command[len(prefix):].strip()

    if argument.startswith('"') or argument.startswith("'"):
        quote = argument[0]
        end = argument.find(quote, 1)

        if end == -1:
            raise ValueError("Please close the quotation marks.")

        return argument[1:end]

    return argument


def main():
    assistant = AURAAssistant()

    print("\n================================")
    print("       AURA AI ASSISTANT")
    print("================================")
    print("\nYour local AI assistant is ready!")

    print("\nCommands:")
    print("/search <query> - Search the web")
    print("/url <website-link> - Read a website")
    print('/file "<file-path>" - Load a PDF or TXT')
    print('/addfile "<file-path>" - Add another document')
    print("/sources - Show loaded sources")
    print('/image "<image-path>" <question> - Analyze an image')
    print("/history - Show saved conversations")
    print("/open <id> - Open an old conversation")
    print("/new - Start a new conversation")
    print("/reset - Clear current conversation context")
    print("/exit - Close AURA AI")

    print("\n================================\n")

    while True:
        user_message = input("You: ").strip()

        if not user_message:
            continue

        command = user_message.lower()

        if command == "/exit":
            print("\nAURA AI: Goodbye!")
            break

        if command == "/new":
            assistant.new_conversation()
            continue

        if command == "/history":
            conversations = get_conversations()

            if not conversations:
                print("\nNo saved conversations.\n")
                continue

            print("\nSaved conversations:")

            for conversation in conversations:
                print(
                    f"ID: {conversation['id']} | "
                    f"{conversation['title']} | "
                    f"{conversation['created_at']}"
                )

            print()
            continue

        if command.startswith("/open "):
            try:
                conversation_id = int(
                    user_message[6:].strip()
                )

                assistant.load_conversation(conversation_id)

                print(
                    f"\nAURA AI: Conversation "
                    f"{conversation_id} loaded!\n"
                )

                for message in assistant.history[1:]:
                    label = (
                        "You" if message["role"] == "user"
                        else "AURA AI"
                    )
                    print(f"{label}: {message['content']}\n")

            except ValueError:
                print("\nPlease provide a valid conversation ID.\n")

            except Exception as error:
                print("\nCould not open conversation:", error, "\n")

            continue

        if command == "/reset":
            assistant.reset_chat()
            assistant.page_context = None
            assistant.web_search_context = None
            assistant.documents = []
            assistant.document_rag = None

            print("\nAURA AI: Current context cleared!\n")
            continue

        if command == "/sources":
            if assistant.documents:
                print("\nLoaded documents:")

                for index, document in enumerate(
                    assistant.documents, start=1
                ):
                    print(f"{index}. {document['filename']}")

            elif assistant.web_search_context:
                print("\nWeb research sources:")

                for index, page in enumerate(
                    assistant.web_search_context["pages"],
                    start=1
                ):
                    print(f"{index}. {page['title']}")
                    print("   ", page["url"])

            elif assistant.page_context:
                print("\nLoaded website:")
                print(assistant.page_context["title"])
                print(assistant.page_context["url"])

            else:
                print("\nNo documents or website loaded.")

            print()
            continue

        if command.startswith("/search "):
            query = user_message[8:].strip()

            try:
                print("\nAURA AI: Searching the web...\n")

                results = search_web(query, max_results=5)

                assistant.set_web_search_context(results)

                print(
                    f"\nFound {len(results['pages'])} readable pages."
                )

                for index, page in enumerate(
                    results["pages"], start=1
                ):
                    print(f"{index}. {page['title']}")
                    print("   ", page["url"])

                print("\nAsk a question about these results.\n")

            except Exception as error:
                print("\nWeb search failed:", error, "\n")

            continue

        if command.startswith("/url "):
            url = user_message[5:].strip()

            try:
                print("\nAURA AI: Reading website...\n")

                page = read_website(url)
                assistant.set_page_context(page)

                print("Website loaded:", page["title"])
                print("Source:", page["url"])
                print()

            except Exception as error:
                print("\nCould not read website:", error, "\n")

            continue

        if command.startswith("/file "):
            try:
                file_path = parse_file_path(user_message, "/file")
                document = read_document(file_path)

                assistant.set_document_context(document)

                print(
                    "\nDocument loaded:",
                    document["filename"],
                    "\n"
                )

            except Exception as error:
                print("\nCould not load document:", error, "\n")

            continue

        if command.startswith("/addfile "):
            try:
                file_path = parse_file_path(user_message, "/addfile")
                document = read_document(file_path)

                assistant.add_document_context(document)

                print(
                    "\nDocument added:",
                    document["filename"],
                    "\n"
                )

            except Exception as error:
                print("\nCould not add document:", error, "\n")

            continue

        if command.startswith("/image "):
            try:
                image_path, question = parse_image_command(user_message)

                assistant.llm.model = None
                gc.collect()

                answer = analyze_image(image_path, question)

                print("\nAURA AI:", answer, "\n")

            except Exception as error:
                print("\nCould not analyze image:", error, "\n")

            continue

        try:
            print("\nAURA AI is thinking...\n")

            answer = assistant.chat(user_message)

            print("AURA AI:", answer, "\n")

        except Exception as error:
            print("\nError:", error, "\n")


if __name__ == "__main__":
    main()
