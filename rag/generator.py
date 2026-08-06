from llm.model import get_llm
from rag.retriever import get_retriever
from llm.relevance_checker import is_relevant

llm = get_llm()
retriever = get_retriever()


def generate_code(question: str):

    docs = retriever.invoke(question)

    context = "\n\n".join(
        doc.page_content
        for doc in docs
    )

    # -----------------------------
    # CASE 1 : Nothing retrieved
    # -----------------------------

    if not docs:

        prompt = f"""
You are an expert software engineer.

The vector database contains no useful documentation.

Answer the user's request using your own programming knowledge.

Generate complete, clean and production-ready code.

User request:

{question}
"""

        return llm.invoke(prompt).content

    # -----------------------------
    # CASE 2 : Retrieved documents
    # -----------------------------

    relevant = is_relevant(question, context)

    # -----------------------------
    # CASE 2A : Retrieved docs are relevant
    # -----------------------------

    if relevant:

        prompt = f"""
You are an expert software engineer.

Use the retrieved documentation as your PRIMARY source.

If the documentation does not contain every implementation detail,
use your own programming knowledge to complete the answer.

Retrieved Documentation

{context}

User Request

{question}

Return:

1. Complete code
2. Best practices
3. Comments when useful
4. Short explanation
"""

        return llm.invoke(prompt).content

    # -----------------------------
    # CASE 2B : Retrieved docs are irrelevant
    # -----------------------------

    prompt = f"""
The retrieved documentation is unrelated.

Ignore it.

Answer using your own programming knowledge.

User Request:

{question}
"""

    return llm.invoke(prompt).content