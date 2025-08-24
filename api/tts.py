import pyttsx3


def generate_tts(text: str, output_file: str):
    # Force espeak driver
    engine = pyttsx3.init(driverName='espeak')

    # Disable event callbacks
    try:
        engine.connect('started-utterance', lambda name: None)
        engine.connect('finished-utterance', lambda name, completed: None)
    except Exception:
        pass

    engine.save_to_file(text, output_file)
    engine.runAndWait()
    engine.stop()  # ensure engine is fully closed
