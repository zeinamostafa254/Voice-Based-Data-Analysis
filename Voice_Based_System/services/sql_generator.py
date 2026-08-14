import re

from services.llm_service import client
from services.llm_service import MODEL


def clean_sql(sql):

    sql = re.sub(

        r"```sql",

        "",

        sql,

        flags=re.IGNORECASE
    )

    sql = sql.replace("```", "")

    return sql.strip()


def generate_sql(question, schema):

    prompt = f"""

You are an SQLite expert.

Table name:

dataset

Schema:

{schema}

Question:

{question}

Rules:

1. Generate only SQLite SQL.

2. Use only existing columns.

3. Return only SQL.

4. Never modify the database.

5. The question may be Arabic or English.

"""

    response = client.chat.completions.create(

        model=MODEL,

        messages=[

            {

                "role": "user",

                "content": prompt
            }
        ],

        temperature=0
    )

    sql = response.choices[0].message.content

    return clean_sql(sql)