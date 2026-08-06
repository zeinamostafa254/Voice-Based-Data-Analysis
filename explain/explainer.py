from llm.model import get_llm
from llm.prompts import EXPLAIN_PROMPT

llm = get_llm()


def explain_code(code: str) -> str:
    """
    Explains the given code using the LLM.
    """

    prompt = EXPLAIN_PROMPT.format(code=code)

    response = llm.invoke(prompt)

    return response.content