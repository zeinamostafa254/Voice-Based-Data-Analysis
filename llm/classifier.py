from llm.model import get_llm

llm = get_llm()


def classify_request(
    user_input: str,
    memory: str = ""
):

    prompt = f"""
You are an Intent Classification Model.

Conversation Memory:

{memory}

User Request:

{user_input}

Your task is to classify the request.

Possible classes:

1. explain
- explain code
- debug
- understand code
- describe algorithm

2. generate
- generate code
- create project
- write code
- implement
- build application

3. tool
- execute code
- run code
- compile
- calculate output

Rules:

Return ONLY ONE WORD.

Allowed outputs:

explain

generate

tool
"""

    response = llm.invoke(prompt)

    answer = response.content.lower().strip()

    if "explain" in answer:
        return "explain"

    if "generate" in answer:
        return "generate"

    if "tool" in answer:
        return "tool"

    return "generate"
    