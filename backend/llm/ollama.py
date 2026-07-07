import os
import requests

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://192.168.1.201:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen3:8b")


def ask_ollama(prompt: str, timeout: int = 180) -> str:
    try:
        r = requests.post(
            f"{OLLAMA_URL}/api/generate",
            json={
                "model": OLLAMA_MODEL,
                "prompt": prompt,
                "stream": False
            },
            timeout=timeout,
        )
        r.raise_for_status()
        return r.json().get("response", "")
    except Exception as e:
        return f"Ollama error: {e}"
