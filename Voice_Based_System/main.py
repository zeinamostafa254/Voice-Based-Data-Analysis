from fastapi import FastAPI

from api.upload import router as upload_router
from api.voice_analysis import router as voice_router

app = FastAPI(

    title="Voice-Based Data Analysis System",

    description="Arabic and English Voice-Based Data Analysis",

    version="1.0"
)

app.include_router(

    upload_router
)

app.include_router(

    voice_router
)


@app.get("/")

def home():

    return {

        "message": "Voice-Based Data Analysis System"
    }