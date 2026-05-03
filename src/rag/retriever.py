import faiss
import numpy as np
from sentence_transformers import SentenceTransformer


INDEX_PATH = "data/knowledge_base/faiss.index"
CHUNKS_PATH = "data/knowledge_base/chunks.npy"


def load_index():
    index = faiss.read_index(INDEX_PATH)
    chunks = np.load(CHUNKS_PATH, allow_pickle=True)
    return index, chunks


def get_embedding_model():
    return SentenceTransformer("all-MiniLM-L6-v2")


def retrieve(query, top_k=3):
    index, chunks = load_index()
    model = get_embedding_model()

    query_embedding = model.encode([query])

    distances, indices = index.search(np.array(query_embedding), top_k)

    results = [
    {
        "text": chunks[i],
        "source": f"knowledge_base_chunk_{i}"
    }
    for i in indices[0]
]

    return results


def generate_answer(query):
    results = retrieve(query)

    context = "\n\n".join(results)

    # 🔥 Simple structured answer generation (LLM-style without API)
    if "timeline" in query.lower():
        answer = "Here is a recommended wedding planning timeline:\n\n"

        for chunk in results:
            if "Weeks Before" in chunk or "timeline" in chunk.lower():
                answer += chunk + "\n\n"

    else:
        answer = "Here is relevant information based on your query:\n\n"
        answer += context

    return {
        "query": query,
        "answer": answer.strip(),
        "sources": results,
    }


if __name__ == "__main__":
    q = "What is the best wedding timeline?"

    result = generate_answer(q)

    print(result["answer"])