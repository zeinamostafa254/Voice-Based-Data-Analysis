import sys
import os
from unittest import loader

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pathlib import Path

from datasets import load_dataset
from langchain_core.documents import Document

from langchain_community.document_loaders import DirectoryLoader
from langchain_community.document_loaders import UnstructuredHTMLLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma

from embeddings.embedding_model import get_embedding_model


DOCUMENT_PATH = "data/documents/python_docs"
CHROMA_PATH = "data/chroma_db"


def create_database():

    if Path(CHROMA_PATH).exists():

        print("Chroma database already exists.")

        return

    print("Loading Python documentation...")

    loader = DirectoryLoader(
        DOCUMENT_PATH,
        glob="**/*.html",
        loader_cls=UnstructuredHTMLLoader,
        show_progress=True,
        )

    python_docs = loader.load()

    print(f"Loaded {len(python_docs)} Python documents.")

    print("Loading HumanEval dataset...")

    dataset = load_dataset(
    "openai/openai_humaneval",
    split="test"
 )

    humaneval_docs = []

    for sample in dataset:

        text = f"""
    Programming Task

    {sample['prompt']}

    Canonical Solution

    {sample['canonical_solution']}
 """

        humaneval_docs.append(

             Document(
              page_content=text,
             metadata={
                "source": "HumanEval",
                "entry_point": sample["entry_point"],
                "dataset": "openai_humaneval",
            },
        )

    )

    print(f"Loaded {len(humaneval_docs)} HumanEval samples.")

    documents = python_docs + humaneval_docs

    print(f"Total loaded documents: {len(documents)}")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
    )

    chunks = splitter.split_documents(documents)
    for chunk in chunks:

        chunk.metadata.setdefault("source", "PythonDocs")
    print(f"Created {len(chunks)} chunks.")

    embedding_model = get_embedding_model()

    Chroma.from_documents(
        documents=chunks,
        embedding=embedding_model,
        persist_directory=CHROMA_PATH,
    )

    print("Vector database created successfully.")


if __name__ == "__main__":
    create_database()