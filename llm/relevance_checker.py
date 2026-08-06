from llm.model import get_llm

llm = get_llm()


def is_relevant(question, context):

    prompt = f"""
You are a relevance evaluator.

Question:

{question}

Retrieved Context:

{context}

Does the context contain enough information to help answer the question?

Answer ONLY:

YES

or

NO
"""

    answer = llm.invoke(prompt).content.strip().upper()

    return answer.startswith("YES")