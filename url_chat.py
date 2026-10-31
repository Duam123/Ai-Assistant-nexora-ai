import requests
from bs4 import BeautifulSoup

from sentence_transformers import SentenceTransformer
from sentence_transformers.util import cos_sim
from transformers import pipeline


# 1. Load models
print("Loading embedding model...")

embedding_model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)

print("Loading local AI model...")

ai = pipeline(
    "text-generation",
    model="Qwen/Qwen2.5-0.5B-Instruct"
)


# 2. Read website
def read_website(url):
    headers = {
        "User-Agent": "Mozilla/5.0 AURA-AI/1.0"
    }

    response = requests.get(
        url,
        headers=headers,
        timeout=20
    )

    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    for element in soup([
        "script",
        "style",
        "nav",
        "footer",
        "header"
    ]):
        element.decompose()

    return soup.get_text(separator=" ", strip=True)


# 3. Split website into chunks
def create_chunks(text, chunk_size=120, overlap=30):
    words = text.split()
    chunks = []

    step = chunk_size - overlap

    for start in range(0, len(words), step):
        chunk = " ".join(words[start:start + chunk_size])

        if chunk:
            chunks.append(chunk)

    return chunks


# 4. Find relevant website information
def search_website(question, chunks, chunk_embeddings):
    question_embedding = embedding_model.encode(question)

    similarities = cos_sim(
        question_embedding,
        chunk_embeddings
    )[0]

    top_indices = similarities.argsort(
        descending=True
    )[:3].tolist()

    relevant_chunks = [
        chunks[index] for index in top_indices
    ]

    return "\n\n".join(relevant_chunks)


# 5. Generate AI answer
def ask_ai(question, context):
    prompt = f"""
You are AURA AI, a helpful research assistant.

Answer the user's question using the website information below.

Rules:
- Give a clear and simple answer.
- Use only information supported by the provided context.
- If the answer is not available, say that the website information
  does not provide a clear answer.
- Do not invent facts.

WEBSITE INFORMATION:
{context}

USER QUESTION:
{question}

ANSWER:
"""

    result = ai(
        [{"role": "user", "content": prompt}],
        max_new_tokens=180,
        do_sample=False
    )

    return result[0]["generated_text"][-1]["content"]


# 6. Start the application
def main():
    url = input(
        "\nPaste the website URL: "
    ).strip()

    if not url.startswith(("https://", "http://")):
        print("Please enter a valid URL starting with http:// or https://")
        return

    try:
        print("\nReading website...")

        website_text = read_website(url)

        if len(website_text.strip()) < 100:
            print("Not enough readable text found on this website.")
            return

        chunks = create_chunks(website_text)

        print(f"Website loaded: {len(chunks)} text chunks")

        print("\nCreating embeddings...")

        chunk_embeddings = embedding_model.encode(chunks)

        print("\nAURA AI is ready!")
        print("Ask questions about the website.")
        print("Type 'exit' to stop.\n")

        while True:
            question = input("You: ").strip()

            if question.lower() in ["exit", "quit"]:
                print("AURA AI: Goodbye!")
                break

            if not question:
                continue

            context = search_website(
                question,
                chunks,
                chunk_embeddings
            )

            answer = ask_ai(question, context)

            print(f"\nAURA AI: {answer}")
            print(f"\nSource: {url}\n")

    except requests.RequestException as error:
        print(f"Website error: {error}")

    except Exception as error:
        print(f"Something went wrong: {error}")


if __name__ == "__main__":
    main()