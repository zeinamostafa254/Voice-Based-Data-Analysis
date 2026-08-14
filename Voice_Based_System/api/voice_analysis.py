from pathlib import Path
import shutil

from fastapi import APIRouter
from fastapi import File
from fastapi import HTTPException
from fastapi import UploadFile

from database.database import get_table_schema

from services.whisper_service import speech_to_text
from services.sql_generator import generate_sql
from services.sql_service import execute_sql
from services.analyzer import explain_result

router = APIRouter(

    prefix="/analysis",

    tags=["Voice Analysis"]
)

UPLOAD_DIR = Path("data/uploads")

UPLOAD_DIR.mkdir(

    parents=True,

    exist_ok=True
)


@router.post("/voice")

async def analyze_voice(

    audio: UploadFile = File(...)
):

    audio_path = UPLOAD_DIR / audio.filename

    with open(audio_path, "wb") as buffer:

        shutil.copyfileobj(

            audio.file,
            buffer
        )

    transcription = speech_to_text(

        str(audio_path)
    )

    question = transcription["text"]

    schema = get_table_schema()

    if not schema:

        raise HTTPException(

            status_code=400,

            detail="No dataset has been uploaded."
        )

    schema_text = "\n".join(

        f"{column[1]} ({column[2]})"

        for column in schema
    )

    sql = generate_sql(

        question,

        schema_text
    )

    result = execute_sql(sql)

    if not result["success"]:

        raise HTTPException(

            status_code=400,

            detail=result["error"]
        )

    explanation = explain_result(

        question,

        result["data"]
    )

    return {

        "language": transcription["language"],

        "question": question,

        "sql": sql,

        "columns": result["columns"],

        "results": result["data"],

        "answer": explanation
    }