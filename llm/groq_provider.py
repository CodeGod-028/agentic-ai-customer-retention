import os
import re
import time

from groq import Groq


class GroqProvider:

    def __init__(self):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.model = "qwen/qwen3.8-27b"

    def generate(self, prompt, max_tokens=400):
        for attempt in range(2):
            try:
                completion = self.client.chat.completions.create(
                    messages=[{"role": "user", "content": prompt}],
                    model=self.model,
                    temperature=0.2,
                    max_tokens=max_tokens,   # the fix: must stay under 1000
                )
                text = completion.choices[0].message.content or ""

                # Some Qwen models print their reasoning inside <think> tags: remove it
                text = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL).strip()
                return text

            except Exception as e:
                # Rate limit: wait for the per-minute window, then try once more
                if "429" in str(e) and attempt == 0:
                    time.sleep(20)
                    continue
                break

        # Starts with "Groq Error" so KnowledgeAgent switches to its fallback answer
        return "Groq Error: the AI service is busy or rate limited. Please try again in a minute."