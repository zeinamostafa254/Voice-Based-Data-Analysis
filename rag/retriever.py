from langchain_chroma import Chroma

from embeddings.embedding_model import get_embedding_model


CHROMA_PATH = "data/chroma_db"


def get_retriever():

    db = Chroma(
        persist_directory=CHROMA_PATH,
        embedding_function=get_embedding_model(),
    )

    return db.as_retriever(
    search_type="mmr",
    search_kwargs={
        "k": 5,
        "fetch_k": 15,
    },
)