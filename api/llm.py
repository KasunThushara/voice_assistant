from ollama import chat

def ask_ollama(question: str) -> str:
    response = chat(model="gemma3:4b", messages=[
        {"role": "user", "content": question},
    ])
    return response.message.content
