"""
Knowledge Agent

RAG Pipeline

Question -> TF-IDF Retrieval -> Relevant Context -> LLM (Groq) -> Business Answer
If the LLM is unavailable or rate limited, the answer is built from the retrieved documents.
"""

import pickle

from sklearn.metrics.pairwise import cosine_similarity

from llm.groq_provider import GroqProvider


class KnowledgeAgent:

    def __init__(self):
        self.vectorizer = None
        self.vectors = None
        self.documents = None
        self.load_rag_assets()
        self.llm = GroqProvider()

    def load_rag_assets(self):
        with open("rag/vectorizer.pkl", "rb") as f:
            self.vectorizer = pickle.load(f)
        with open("rag/vectors.pkl", "rb") as f:
            self.vectors = pickle.load(f)
        with open("rag/documents.pkl", "rb") as f:
            self.documents = pickle.load(f)

    def retrieve_context(self, question, top_k=3):
        query_vector = self.vectorizer.transform([question])
        similarities = cosine_similarity(query_vector, self.vectors)[0]
        top_idx = similarities.argsort()[-top_k:][::-1]
        # Skip documents with no word overlap at all
        return [self.documents[i] for i in top_idx if similarities[i] > 0]

    def build_prompt(self, question, retrieved_docs):
        # Trim each document: fewer input tokens, faster answers
        context = "\n\n".join(d[:800] for d in retrieved_docs[:3])

        return f"""
You are a Customer Retention AI Advisor.

Use only the provided business context.

BUSINESS CONTEXT
----------------
{context}

QUESTION
--------
{question}

Instructions:
- Answer professionally.
- Be concise: at most 120 words.
- Provide executive recommendations.
- Mention supporting evidence.
"""

    def fallback_answer(self, docs):
        # Used when the LLM fails: answer straight from the retrieved documents
        if not docs:
            return "No relevant information was found in the business documents."
        top = [d.strip()[:600] for d in docs[:2]]
        return "Based on the business documents:\n\n" + "\n\n".join(top)

    def ask(self, question):
        context_docs = self.retrieve_context(question)

        if not context_docs:
            return {"answer": self.fallback_answer([]), "sources": []}

        prompt = self.build_prompt(question, context_docs)
        answer = self.llm.generate(prompt)

        # The provider returns None (or an error string) when Groq fails
        if not answer or str(answer).startswith("Groq Error"):
            answer = self.fallback_answer(context_docs)

        return {"answer": answer, "sources": context_docs}


if __name__ == "__main__":
    agent = KnowledgeAgent()
    result = agent.ask("Which retention strategy works best for loyal customers?")
    print("=" * 70)
    print("KNOWLEDGE AGENT")
    print("=" * 70)
    print(result["answer"])