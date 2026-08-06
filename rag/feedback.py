from uuid import uuid4

from langchain_core.documents import Document
from langchain_chroma import Chroma
from datetime import datetime
from embeddings.embedding_model import get_embedding_model

CHROMA_PATH = "data/chroma_db"


def learn_from_feedback(question: str, solution: str):

    db = Chroma(
        persist_directory=CHROMA_PATH,
        embedding_function=get_embedding_model(),
    )

    # Prevent duplicates
    existing = db.similarity_search(
        solution,
        k=1,
    )

    if existing:

        if existing[0].page_content == solution:

            return "Knowledge already exists."

    document = Document(

        page_content=f"""
Question

{question}

Solution

{solution}
""",

        metadata={

    "source": "user_feedback",

    "type": "feedback",

    "intent": "generate",

    "language": "python",

    "framework": "unknown",

    "timestamp": datetime.now().isoformat(),

    "user_verified": True

   }

    )

    db.add_documents(
        documents=[document],
        ids=[str(uuid4())]
    )

    return "Knowledge learned successfully."