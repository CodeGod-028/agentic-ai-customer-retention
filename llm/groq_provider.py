import os

from groq import Groq


class GroqProvider:

    def __init__(self):

        self.client = Groq(
            api_key=os.getenv(
                "GROQ_API_KEY"
            )
        )

        self.model = (
            "qwen/qwen3.8-27b"
        )

    def generate(
        self,
        prompt
    ):

        try:

            completion = (
                self.client.chat.completions.create(
                    messages=[
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    model=self.model
                )
            )

            return (
                completion
                .choices[0]
                .message
                .content
            )

        except Exception as e:

            return (
                f"Groq Error: {str(e)}"
            )