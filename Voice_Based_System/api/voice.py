from pathlib import Path

import shutil

from fastapi import APIRouter
from fastapi import File
from fastapi import UploadFile

from services.whisper_service import speech_to_text

router = APIRouter(

    prefix="/voice",

    tags=["Voice"]
)

UPLOAD_DIR = Path(

    "data/uploads"
)

UPLOAD_DIR.mkdir(

    parents=True,

    exist_ok=True
)


@router.post("/transcribe")

async def transcribe(

    audio: UploadFile = File(...)
):

    path = UPLOAD_DIR / audio.filename

    with open(path, "wb") as buffer:

        shutil.copyfileobj(

            audio.file,

            buffer
        )

    return speech_to_text(path)