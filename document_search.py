from sentence_transformers import SentenceTransformer
from sentence_transformers.util import cos_sim

# 1. Read the document
with open("knowledge.txt", "r", encoding="utf-8") as file:
    text = file.read()

# 2. Split the document into chunks
chunks = [line.strip() for line in text.split("\n") if line.strip()]

# 3. Load the embedding model
embedding_model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)

# 4. Convert chunks into embeddings
chunk_embeddings = embedding_model.encode(chunks)

# 5. Ask a question
question = "How does RAG work?"

# 6. Convert the question into an embedding
question_embedding = embedding_model.encode(question)

# 7. Compare the question with all chunks
similarities = cos_sim(
    question_embedding,
    chunk_embeddings
)[0]

# 8. Find the most relevant chunk
best_index = similarities.argmax().item()

print("\nAURA AI - Document Search")
print("Question:", question)
print("\nRelevant information:")
print(chunks[best_index])
print("\nSimilarity score:", round(similarities[best_index].item(), 4))