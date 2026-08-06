from explain.explainer import explain_code
from rag.generator import generate_code
from tools.code_executor import execute_code


def route(
    user_input: str,
    intent: str,
    memory: str = "",
):

    if not user_input.strip():
        return "Please enter a request."

    intent = intent.lower()

    if intent == "explain":
        return explain_code(
            user_input,
            memory
        )

    elif intent == "generate" or intent == "create" or intent == "implement" or intent == "project" or intent == "make":
        return generate_code(
            user_input,
            memory
        )

    elif intent == "tool":
        return execute_code(user_input)

    return "Unable to determine the request type."