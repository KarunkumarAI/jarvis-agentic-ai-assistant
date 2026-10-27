from langchain_google_genai import GoogleGenerativeAIEmbeddings

from core.config import GOOGLE_API_KEY


def get_embeddings() -> GoogleGenerativeAIEmbeddings:
    return GoogleGenerativeAIEmbeddings(
        model="gemini-embedding-2",
        google_api_key=GOOGLE_API_KEY,
    )