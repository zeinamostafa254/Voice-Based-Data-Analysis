import re

from database.database import get_connection


FORBIDDEN_KEYWORDS = [

    "INSERT",

    "UPDATE",

    "DELETE",

    "DROP",

    "ALTER",

    "CREATE",

    "REPLACE",

    "ATTACH",

    "DETACH",

    "PRAGMA"
]


def validate_sql(query):

    query = query.strip()

    if not query:

        return False, "Empty query."

    normalized = query.upper()

    normalized = normalized.rstrip(";")

    if not normalized.startswith(

        ("SELECT", "WITH")
    ):

        return False, "Only SELECT statements are allowed."

    for keyword in FORBIDDEN_KEYWORDS:

        if re.search(

            rf"\b{keyword}\b",

            normalized
        ):

            return False, f"Forbidden command: {keyword}"

    return True, None


def execute_sql(query):

    valid, error = validate_sql(query)

    if not valid:

        return {

            "success": False,

            "error": error
        }

    connection = get_connection()

    cursor = connection.cursor()

    try:

        cursor.execute(query)

        rows = cursor.fetchall()

        columns = [

            description[0]

            for description

            in cursor.description
        ]

        return {

            "success": True,

            "columns": columns,

            "data": rows,

            "row_count": len(rows)
        }

    except Exception as e:

        return {

            "success": False,

            "error": str(e)
        }

    finally:

        connection.close()