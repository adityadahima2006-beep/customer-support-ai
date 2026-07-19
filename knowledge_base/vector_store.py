import os
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# ---------------------------------
# Load Embedding Model
# ---------------------------------
try:
    model = SentenceTransformer("all-MiniLM-L6-v2")
except Exception as e:
    raise RuntimeError(f"Failed to load embedding model: {e}")

# ---------------------------------
# Knowledge Base Folder
# ---------------------------------
BASE_PATH = os.path.dirname(__file__)

documents = []
file_names = []

# ---------------------------------
# Load TXT Files
# ---------------------------------
for file in os.listdir(BASE_PATH):

    if file.endswith(".txt"):

        file_path = os.path.join(BASE_PATH, file)

        try:
            with open(file_path, "r", encoding="utf-8") as f:

                text = f.read().strip()

                if text:
                    documents.append(text)
                    file_names.append(file)

        except Exception as e:
            print(f"Error reading {file}: {e}")

# ---------------------------------
# Create FAISS Index
# ---------------------------------
index = None

if documents:

    embeddings = model.encode(documents)

    embeddings = np.array(embeddings).astype("float32")

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatL2(dimension)

    index.add(embeddings)

else:

    print("WARNING: No knowledge base documents found.")

# ---------------------------------
# Search Function
# ---------------------------------
def search(query, top_k=3, threshold=2.0):
    """
    Search the knowledge base.

    Returns:
        list of relevant documents
    """

    if index is None:
        return []

    try:

        query_embedding = model.encode([query])

        query_embedding = np.array(query_embedding).astype("float32")

        distances, indices = index.search(
            query_embedding,
            top_k
        )

        results = []

        for distance, idx in zip(distances[0], indices[0]):

            if idx == -1:
                continue

            if idx >= len(documents):
                continue

            if distance > threshold:
                continue

            results.append(
                {
                    "file": file_names[idx],
                    "content": documents[idx],
                    "score": float(distance)
                }
            )

        return results

    except Exception as e:

        print(f"Knowledge Base Search Error: {e}")

        return []
