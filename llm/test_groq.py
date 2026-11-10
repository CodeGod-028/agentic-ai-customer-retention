from llm.groq_provider import (
    GroqProvider
)

provider = GroqProvider()

response = provider.generate(
    """
    Give a customer retention
    recommendation for a
    high-risk customer.
    """
)

print(response)