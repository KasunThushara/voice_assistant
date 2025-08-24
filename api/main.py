from fastapi import FastAPI, File, UploadFile, Header, HTTPException
import uuid
import os
import traceback

from stt import stt_from_file   # now this talks to vosk server via HTTP
from llm import ask_ollama
from tts import generate_tts

API_KEYS = {"test123"}  # replace with DB later
app = FastAPI()


@app.post("/process")
async def process_audio(file: UploadFile = File(...), api_key: str = Header(None)):
    print("Received request")

    if api_key not in API_KEYS:
        print(f"Invalid API key: {api_key}")
        raise HTTPException(status_code=401, detail="Invalid API key")

    temp_filename = f"/tmp/temp_{uuid.uuid4()}.wav"  # use /tmp for safe container write
    try:
        print(f"Saving uploaded file to {temp_filename}")
        with open(temp_filename, "wb") as f:
            f.write(await file.read())
        print("File saved successfully")
    except Exception as e:
        print("Error saving uploaded file:", e)
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"File save error: {e}")

    try:
        print("Running STT (via Vosk server)...")
        question = stt_from_file(temp_filename)
        print("STT result:", question)
    except Exception as e:
        print("Error in STT:", e)
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"STT error: {e}")

    try:
        print("Querying Ollama LLM...")
        answer = ask_ollama(question)
        print("LLM answer:", answer)
    except Exception as e:
        print("Error in LLM:", e)
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"LLM error: {e}")

    output_wav = f"/tmp/response_{uuid.uuid4()}.wav"
    try:
        print("Generating TTS...")
        generate_tts(answer, output_wav)
        print(f"TTS file created: {output_wav}")
    except Exception as e:
        print("Error in TTS:", e)
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"TTS error: {e}")

    return {
        "transcript": question,
        "answer": answer,
        "audio_file": output_wav
    }
