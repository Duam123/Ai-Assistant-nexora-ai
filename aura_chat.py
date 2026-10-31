
from transformers import pipeline

# 1. AURA AI personality
SYSTEM_PROMPT = """
You are AURA AI, a helpful and intelligent personal AI assistant.

Your responsibilities:
- Answer general knowledge questions.
- Explain programming and technical concepts.
- Help with education, research and problem solving.
- Write emails, documents and creative content.
- Help users understand AI and software engineering.

Behavior:
- Be friendly, professional and conversational.
- Give clear and useful answers.
- Use simple language when explaining difficult topics.
- Provide examples when helpful.
- If you do not know something, be honest.
- Never pretend to have accessed live internet information.
- Remember the context of the current conversation.
"""

# 2. Load the local model once
print("\nLoading AURA AI... Please wait.")

ai = pipeline(
    "text-generation",
    model="Qwen/Qwen2.5-0.5B-Instruct"
)

print("\nAURA AI is ready!")
print("Type /reset to start a new conversation.")
print("Type /exit to close AURA AI.\n")


# 3. Store conversation history
messages = [
    {
        "role": "system",
        "content": SYSTEM_PROMPT
    }
]


# 4. Chat loop
while True:

    user_input = input("You: ").strip()

    if not user_input:
        continue

    if user_input.lower() == "/exit":
        print("\nAURA AI: Goodbye! Have a great day.")
        break

    if user_input.lower() == "/reset":
        messages = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            }
        ]

        print("\nAURA AI: New conversation started!\n")
        continue

    # Add user message to history
    messages.append({
        "role": "user",
        "content": user_input
    })

    try:
        print("\nAURA AI is thinking...\n")

        result = ai(
            messages,
            max_new_tokens=160,
            do_sample=False
        )

        # Get the latest AI response
        conversation = result[0]["generated_text"]

        answer = conversation[-1]["content"]

        # Add AI response to history
        messages.append({
            "role": "assistant",
            "content": answer
        })

        print("AURA AI:", answer, "\n")

        # Keep recent conversation to control memory usage
        if len(messages) > 9:
            messages = [messages[0]] + messages[-8:]

    except Exception as error:
        # Remove the unanswered user message
        messages.pop()

        print("Error:", error, "\n")
