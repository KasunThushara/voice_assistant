from fastapi import FastAPI, File, UploadFile, Header, HTTPException
import uuid
import os

from stt import stt_from_file
from llm import ask_ollama
from tts import generate_tts

API_KEYS = {"test123"}  # replace with DB later
app = FastAPI()

@app.post("/process")
async def process_audio(file: UploadFile = File(...), api_key: str = Header(None)):
    if api_key not in API_KEYS:
        raise HTTPException(status_code=401, detail="Invalid API key")

    temp_filename = f"temp_{uuid.uuid4()}.wav"
    with open(temp_filename, "wb") as f:
        f.write(await file.read())

    # 1. STT
    question = stt_from_file(temp_filename)

    # 2. LLM
    answer = ask_ollama(question)

    # 3. TTS
    output_wav = f"response_{uuid.uuid4()}.wav"
    generate_tts(answer, output_wav)

    return {
        "transcript": question,
        "answer": answer,
        "audio_file": output_wav
    }
