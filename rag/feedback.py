from uuid import uuid4

from langchain_core.documents import Document
from langchain_chroma import Chroma

from embeddings.embedding_model import get_embedding_model


CHROMA_PATH = "data/chroma_db"


def learn(question, answer):

    db = Chroma(
        persist_directory=CHROMA_PATH,
        embedding_function=get_embedding_model(),
    )

    doc = Document(

        page_content=f"""

Question

{question}

Answer

{answer}

""",

        metadata={
            "source": "user_feedback",
            "type": "feedback"
        }

    )

    db.add_documents(
        [doc],
        ids=[str(uuid4())]
    )

    return "Knowledge saved successfully."
    