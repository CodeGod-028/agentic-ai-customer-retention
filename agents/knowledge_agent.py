"""
Knowledge Agent

RAG Pipeline

Question
    ↓
TF-IDF Retrieval
    ↓
Relevant Context
    ↓
Gemini
    ↓
Business Answer
"""

import os
import pickle

import pandas as pd

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

        with open(
            "rag/vectorizer.pkl",
            "rb"
        ) as f:

            self.vectorizer = pickle.load(f)

        with open(
            "rag/vectors.pkl",
            "rb"
        ) as f:

            self.vectors = pickle.load(f)

        with open(
            "rag/documents.pkl",
            "rb"
        ) as f:

            self.documents = pickle.load(f)

    def retrieve_context(
        self,
        question,
        top_k=3
    ):

        query_vector = (
            self.vectorizer
            .transform([question])
        )

        similarities = cosine_similarity(
            query_vector,
            self.vectors
        )[0]

        top_idx = (
            similarities.argsort()
            [-top_k:]
            [::-1]
        )

        results = []

        for idx in top_idx:

            results.append(
                self.documents[idx]
            )

        return results

    def build_prompt(
        self,
        question,
        retrieved_docs
    ):

        context = "\n\n".join(
            retrieved_docs
        )

        prompt = f"""
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
- Be concise.
- Provide executive recommendations.
- Mention supporting evidence.
"""

        return prompt

    def ask(
        self,
        question
    ):

        context_docs = (
            self.retrieve_context(
                question
            )
        )

        prompt = self.build_prompt(
            question,
            context_docs
        )

        answer = self.llm.generate(
            prompt
        )

        return {
            "answer": answer,
            "sources": context_docs
        }


if __name__ == "__main__":

    agent = KnowledgeAgent()

    result = agent.ask(
        "Which retention strategy works best for loyal customers?"
    )

    print("\n")
    print("=" * 70)
    print("KNOWLEDGE AGENT")
    print("=" * 70)

    print(result["answer"])