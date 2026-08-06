from datasets import load_dataset
from langchain_core.documents import Document
from langchain_chroma import Chroma

from embeddings.embedding_model import get_embedding_model

CHROMA_PATH = "data/chroma_db"

dataset = load_dataset("openai/openai_humaneval", split="test")

db = Chroma(
    persist_directory=CHROMA_PATH,
    embedding_function=get_embedding_model(),
)

documents = []

for sample in dataset:

    text = f"""
Programming Task

{sample['prompt']}

Canonical Solution

{sample['canonical_solution']}
"""

    doc = Document(
        page_content=text,
        metadata={
            "source": "HumanEval",
            "entry_point": sample["entry_point"],
            "dataset": "openai_humaneval",
        },
    )

    documents.append(doc)

print(f"Loaded {len(documents)} documents")

db.add_documents(documents)

print("HumanEval added successfully.")
