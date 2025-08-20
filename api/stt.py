import wave
import json
from vosk import Model, KaldiRecognizer

model = Model("vosk-model-small-en-us-0.15")  # download locally or mount volume

def stt_from_file(filename: str) -> str:
    wf = wave.open(filename, "rb")
    if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getframerate() != 16000:
        raise ValueError("Audio file must be Mono PCM 16-bit 16kHz")

    rec = KaldiRecognizer(model, wf.getframerate())
    text = ""
    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            part = json.loads(rec.Result())["text"]
            text += " " + part
    final = json.loads(rec.FinalResult())["text"]
    text += " " + final
    return text.strip()
