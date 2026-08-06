from langchain_openai import ChatOpenAI

from config import (
    OPENROUTER_API_KEY,
    BASE_URL,
    MODEL_NAME,
    TEMPERATURE,
)

# Create the LLM once
llm = ChatOpenAI(
    model=MODEL_NAME,
    api_key=OPENROUTER_API_KEY,
    base_url=BASE_URL,
    temperature=TEMPERATURE,
)


def get_llm():
    """
    Return the configured language model.
    """
    return llm