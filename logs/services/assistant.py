from router import route
from llm.classifier import classify_request
from memory.memory import get_memory, add_interaction


def process_request(user_input: str):

    # Load conversation memory
    memory = get_memory()

    # Detect user intent
    intent = classify_request(user_input, memory)

    # Route request
    response = route(
        user_input=user_input,
        intent=intent,
        memory=memory,
    )

    # Save interaction
    add_interaction(
        question=user_input,
        answer=response,
    )

    return response