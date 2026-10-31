
from sentence_transformers import SentenceTransformer, util


class DocumentRAG:

    def __init__(self, documents):
        print("\nNEXORA AI: Preparing documents for RAG...")

        self.model = SentenceTransformer(
            "sentence-transformers/all-MiniLM-L6-v2"
        )

        self.chunks = []

        for document in documents:
            filename = document.get("filename", "Unknown document")

            for page in document.get("pages", []):
                page_number = page.get("page", "Unknown")
                page_text = page.get("text", "")

                if not isinstance(page_text, str):
                    continue

                words = page_text.split()

                chunk_size = 800
                overlap = 120
                start = 0

                while start < len(words):
                    end = start + chunk_size
                    chunk_text = " ".join(words[start:end])

                    if chunk_text.strip():
                        self.chunks.append({
                            "text": chunk_text,
                            "filename": filename,
                            "page": page_number
                        })

                    start += chunk_size - overlap

        if not self.chunks:
            raise ValueError("No searchable text found in documents.")

        texts = [chunk["text"] for chunk in self.chunks]

        self.embeddings = self.model.encode(
            texts,
            convert_to_tensor=True,
            show_progress_bar=False
        )

        print(f"RAG ready! Indexed {len(self.chunks)} chunks.")

    def search(self, question, top_k=4):

        question_embedding = self.model.encode(
            question,
            convert_to_tensor=True
        )

        scores = util.cos_sim(
            question_embedding,
            self.embeddings
        )[0]

        result_count = min(top_k, len(self.chunks))
        top_results = scores.topk(result_count)

        retrieved_chunks = []

        for score, index in zip(
            top_results.values,
            top_results.indices
        ):
            chunk = self.chunks[index.item()]

            retrieved_chunks.append({
                "text": chunk["text"],
                "filename": chunk["filename"],
                "page": chunk["page"],
                "score": score.item()
            })

        return retrieved_chunks
