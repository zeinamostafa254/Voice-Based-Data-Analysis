from fastapi import APIRouter
from pydantic import BaseModel

from database.database import get_table_schema

from services.analyzer import explain_result
from services.sql_generator import generate_sql
from services.sql_service import execute_sql

router = APIRouter(

    prefix="/analysis",

    tags=["Analysis"]
)


class Question(BaseModel):

    question: str


@router.post("/")

async def analyze(

    request: Question
):

    schema = get_table_schema()

    schema_text = "\n".join(

        f"{column[1]} ({column[2]})"

        for column

        in schema
    )

    sql = generate_sql(

        request.question,

        schema_text
    )

    result = execute_sql(sql)

    result["sql"] = sql

    result["explanation"] = explain_result(result)

    return result