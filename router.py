from explain.explainer import explain_code
from rag.generator import generate_code


def route(user_input: str, mode: str = "explain") -> str:

    if not user_input.strip():
        return "Please enter something."

    if mode == "explain":
        return explain_code(user_input)

    elif mode == "generate":
        return generate_code(user_input)

    else:
        return "Unknown mode."