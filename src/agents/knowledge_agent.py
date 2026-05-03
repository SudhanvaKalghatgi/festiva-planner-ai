from src.rag.retriever import retrieve


def knowledge_agent(query: str):
    results = retrieve(query)

    # Extract text cleanly from structured results
    context = "\n\n".join([r["text"] for r in results])

    # 🔥 Clean response generation (no fragile filtering)
    if "timeline" in query.lower():
        answer = "Here is a recommended wedding planning timeline:\n\n"
        answer += context
    else:
        answer = "Here is relevant information:\n\n"
        answer += context

    # 🔥 Proper citations
    citations = [r["source"] for r in results]

    return {
        "query": query,
        "answer": answer.strip(),
        "citations": citations,
        "confidence": round(1 / len(results), 2),
    }


if __name__ == "__main__":
    q = "best wedding timeline"

    result = knowledge_agent(q)

    print(result)