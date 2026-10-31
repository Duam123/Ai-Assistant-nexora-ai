
from transformers import pipeline

generator = pipeline(
    "text-generation",
    model="Qwen/Qwen2.5-0.5B-Instruct"
)

messages = [
    {
        "role": "user",
        "content": "Explain artificial intelligence in simple words."
    }
]

result = generator(
    messages,
    max_new_tokens=100,
    do_sample=False
)

answer = result[0]["generated_text"][-1]["content"]

print("\nAURA AI - LLM Test")
print(answer)
