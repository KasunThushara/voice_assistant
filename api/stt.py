# Alternative implementation using synchronous WebSocket
import json
import wave
import websocket
import threading


VOSK_SERVER_URL = "ws://vosk:2700/"

def stt_from_file(filename: str) -> str:
    wf = wave.open(filename, "rb")
    if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getframerate() != 16000:
        raise ValueError("Audio file must be Mono PCM 16-bit 16kHz")

    try:
        ws = websocket.create_connection(VOSK_SERVER_URL)

        # Send initial configuration
        config = {
            "config": {
                "sample_rate": wf.getframerate(),
                "words": True
            }
        }
        ws.send(json.dumps(config))

        # Send audio data in chunks
        while True:
            data = wf.readframes(4000)
            if not data:
                break
            # Send as binary data - data is already bytes from wave.readframes()
            ws.send(data, websocket.ABNF.OPCODE_BINARY)

        # Signal end of stream
        ws.send(json.dumps({"eof": 1}))

        # Collect results
        results = []
        while True:
            try:
                message = ws.recv()
                if not message:
                    break

                res = json.loads(message)
                print(f"Received: {res}")  # Debug

                # Collect text from results
                if "text" in res and res["text"].strip():
                    results.append(res["text"].strip())

                # Check if this is the final result
                if res.get("final", False):
                    break

            except json.JSONDecodeError as e:
                print(f"JSON decode error: {e}")
                break
            except Exception as e:
                print(f"Error receiving message: {e}")
                break

        ws.close()
        return " ".join(results).strip()

    except Exception as e:
        print(f"Connection error: {e}")
        return ""
    finally:
        wf.close()