
from transformers import pipeline


class LocalLLM:

    def __init__(self):
        self.model = None

    def load_model(self):

        if self.model is None:

            print("\nLoading NEXORA AI language model...")

            self.model = pipeline(
                "text-generation",
                model="Qwen/Qwen2.5-0.5B-Instruct",
                device=-1
            )

            print("NEXORA AI language model loaded!")

    def generate(self, messages):

        self.load_model()

        result = self.model(
            messages,
            max_new_tokens=400,
            do_sample=False
        )

        generated = result[0]["generated_text"]

        if isinstance(generated, list):
            answer = generated[-1]["content"]
        else:
            answer = str(generated)

        return answer.strip()
