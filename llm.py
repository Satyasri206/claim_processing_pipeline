import os
from langchain_community.llms import Ollama

OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3")

def get_llm():
    return Ollama(
        model=OLLAMA_MODEL,
        temperature=0.0
    )
