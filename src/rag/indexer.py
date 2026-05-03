import os
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer


DATA_PATH = "data/knowledge_base"
INDEX_PATH = "data/knowledge_base/faiss.index"
CHUNKS_PATH = "data/knowledge_base/chunks.npy"


def load_documents():
    documents = []

    for file in os.listdir(DATA_PATH):
        if file.endswith(".txt"):
            with open(os.path.join(DATA_PATH, file), "r", encoding="utf-8") as f:
                documents.append(f.read())

    return documents


# 🔥 FIXED CHUNKING (sentence-aware, no broken words)
def chunk_text(text, chunk_size=400, overlap=50):
    paragraphs = text.split("\n\n")  # split by paragraph
    chunks = []
    current_chunk = ""

    for para in paragraphs:
        if len(current_chunk) + len(para) < chunk_size:
            current_chunk += para + "\n\n"
        else:
            chunks.append(current_chunk.strip())
            current_chunk = para + "\n\n"

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks


def create_chunks(documents):
    all_chunks = []

    for doc in documents:
        chunks = chunk_text(doc)
        all_chunks.extend(chunks)

    return all_chunks


def build_index(chunks):
    model = SentenceTransformer("all-MiniLM-L6-v2")

    embeddings = model.encode(chunks)

    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)

    index.add(np.array(embeddings))

    return index


def save_index(index, chunks):
    faiss.write_index(index, INDEX_PATH)
    np.save(CHUNKS_PATH, chunks)
    print("FAISS index saved successfully")


def main():
    documents = load_documents()

    chunks = create_chunks(documents)
    print(f"Total chunks created: {len(chunks)}")

    index = build_index(chunks)

    save_index(index, chunks)


if __name__ == "__main__":
    main()