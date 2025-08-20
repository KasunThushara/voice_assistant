import pyttsx3

def generate_tts(text: str, output_file: str):
    engine = pyttsx3.init()
    engine.save_to_file(text, output_file)
    engine.runAndWait()
