from pathlib import Path

from langchain_qdrant import QdrantVectorStore

from rag.embeddings import get_embeddings


QDRANT_PATH = "data/qdrant"
COLLECTION_NAME = "jarvis_documents"


def create_vector_store(documents) -> QdrantVectorStore:
    Path(QDRANT_PATH).mkdir(parents=True, exist_ok=True)

    return QdrantVectorStore.from_documents(
        documents=documents,
        embedding=get_embeddings(),
        path=QDRANT_PATH,
        collection_name=COLLECTION_NAME,
    )


def load_vector_store() -> QdrantVectorStore:
    return QdrantVectorStore.from_existing_collection(
        embedding=get_embeddings(),
        path=QDRANT_PATH,
        collection_name=COLLECTION_NAME,
    )