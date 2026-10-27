from rag.vector_store import load_vector_store


def retrieve_documents(question: str, k: int = 4):
    vector_store = load_vector_store()

    return vector_store.similarity_search(
        query=question,
        k=k,
    )