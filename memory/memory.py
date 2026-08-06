conversation = []


def add_interaction(
    question,
    answer,
):

    conversation.append(
        {
            "question": question,
            "answer": answer,
        }
    )


def get_memory():

    if not conversation:
        return ""

    memory = ""

    for item in conversation[-5:]:

        memory += f"""

User:

{item['question']}

Assistant:

{item['answer']}

"""

    return memory
    