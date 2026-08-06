from router import route
from llm.classifier import classify_request


def process_request(user_input: str) -> str:
    """
    Main assistant pipeline.
    """

    mode = classify_request(user_input)

    return route(user_input, mode)