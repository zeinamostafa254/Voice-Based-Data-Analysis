'''def explain_result(result):

    if result["row_count"] == 0:

        return "No matching records were found."

    return f"{result['row_count']} rows were returned."'''

import json

from services.llm_service import client
from services.llm_service import MODEL


def explain_result(question, data):

    if not data:

        return "No matching records were found."

    prompt = f"""
The following question was asked:

{question}

The following data was returned:

{json.dumps(data, ensure_ascii=False)}

Explain the results.

If the question is written in Arabic,
answer in Arabic.

If the question is written in English,
answer in English.

Keep the answer short.
"""

    response = client.chat.completions.create(

        model=MODEL,

        messages=[

            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content