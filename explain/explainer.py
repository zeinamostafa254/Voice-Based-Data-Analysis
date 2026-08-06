from llm.model import get_llm
from llm.prompts import EXPLAIN_PROMPT

llm = get_llm()


def explain_code(
    user_input,
    memory=""
):
    """
    Explains the given code using the LLM.
    
    """

    prompt = EXPLAIN_PROMPT.format(code=user_input, memory=memory)

    response = llm.invoke(prompt)

    return response.content

