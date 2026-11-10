import os
import pickle

from sklearn.feature_extraction.text import (
    TfidfVectorizer
)


DOCUMENT_FILES = [

    "data/retention_policy.txt",

    "data/campaign_history.txt",

    "data/customer_segment_profiles.txt",

    "data/offers.txt",

    "data/brand_guidelines.txt"
]


documents = []

for file in DOCUMENT_FILES:

    with open(
        file,
        "r",
        encoding="utf-8"
    ) as f:

        documents.append(
            f.read()
        )

vectorizer = TfidfVectorizer(
    stop_words="english"
)

vectors = vectorizer.fit_transform(
    documents
)

os.makedirs(
    "rag",
    exist_ok=True
)

with open(
    "rag/vectorizer.pkl",
    "wb"
) as f:

    pickle.dump(
        vectorizer,
        f
    )

with open(
    "rag/vectors.pkl",
    "wb"
) as f:

    pickle.dump(
        vectors,
        f
    )

with open(
    "rag/documents.pkl",
    "wb"
) as f:

    pickle.dump(
        documents,
        f
    )

print(
    "RAG assets generated successfully."
)