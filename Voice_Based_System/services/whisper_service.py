'''from faster_whisper import WhisperModel


MODEL_SIZE = "small"


model = WhisperModel(
    MODEL_SIZE,
    device="cpu",
    compute_type="int8"
)


def speech_to_text(audio_path: str):
    """
    Convert speech audio into text using Faster-Whisper.

    language=None allows Whisper to automatically detect
    the spoken language, including Arabic.
    """

    segments, info = model.transcribe(
        audio_path,
        language=None,
        beam_size=5
    )

    text_parts = []

    for segment in segments:
        text_parts.append(segment.text)

    text = " ".join(text_parts).strip()

    return {
        "text": text,
        "language": info.language
    }'''

#new 
from faster_whisper import WhisperModel

MODEL_SIZE = "small"

model = WhisperModel(

    MODEL_SIZE,

    device="cpu",

    compute_type="int8"
)


def speech_to_text(audio_path):

    segments, info = model.transcribe(

        audio_path,

        language=None,

        beam_size=5
    )

    text = " ".join(

        segment.text

        for segment in segments
    )

    return {

        "text": text.strip(),

        "language": info.language
    }