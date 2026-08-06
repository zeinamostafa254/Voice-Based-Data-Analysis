from llm.model import get_llm


llm = get_llm()


def classify_request(user_input: str) -> str:
    """
    Classifies the user's request.

    Returns:
    - explain
    - generate
    - tool
    """

    prompt = f"""
You are an AI coding assistant router.

Classify the user's request into one category only:

explain:
- User wants code explanation, debugging, or understanding.

generate:
- User wants code creation, project ideas, or implementation.

tool:
- User wants to run code or use a tool.

Return only one word.

User request:
{user_input}
"""

    response = llm.invoke(prompt)

    return response.content.strip().lower()