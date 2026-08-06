from langchain_openai import OpenAIEmbeddings

from config import (
    OPENROUTER_API_KEY,
    BASE_URL,
)


def get_embedding_model():
    """
    Returns the embedding model used to build and query ChromaDB.
    """

    return OpenAIEmbeddings(
        api_key=OPENROUTER_API_KEY,
        base_url=BASE_URL,
        model="text-embedding-3-small",
    )