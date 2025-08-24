import os
from ollama import Client

# get host from env (fallback to local if not set)
ollama_host = os.getenv("OLLAMA_HOST", "http://localhost:11434")

client = Client(host=ollama_host)

def ask_ollama(question: str) -> str:
    response = client.chat(model="gemma2:2b", messages=[
        {"role": "user", "content": question},
    ])
    return response.message.content
