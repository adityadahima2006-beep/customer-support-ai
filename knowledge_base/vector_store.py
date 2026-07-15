import os
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Knowledge Base path
BASE_PATH = os.path.dirname(__file__)

documents = []
file_names = []

# Read all txt files
for file in os.listdir(BASE_PATH):

    if file.endswith(".txt"):

        path = os.path.join(BASE_PATH, file)

        with open(path, "r", encoding="utf-8") as f:

            text = f.read().strip()

            # Skip empty files
            if text:

                documents.append(text)
                file_names.append(file)

# Create embeddings
embeddings = model.encode(documents)

# Create FAISS index
dimension = embeddings.shape[1]

index = faiss.IndexFlatL2(dimension)

index.add(np.array(embeddings).astype("float32"))


def search(query, top_k=1, threshold=1.2):
    """
    Search the knowledge base.
    Returns only relevant results.
    """

    query_embedding = model.encode([query])

    distances, indices = index.search(
        np.array(query_embedding).astype("float32"),
        top_k
    )

    results = []

    for distance, idx in zip(distances[0], indices[0]):

        if idx == -1:
            continue

        # Ignore weak matches
        if distance > threshold:
            continue

        results.append({
            "file": file_names[idx],
            "content": documents[idx],
            "score": float(distance)
        })

    return results
