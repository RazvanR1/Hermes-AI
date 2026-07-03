from core.intent import detect

def route(request: str):
    detected = detect(request)
    return {
        "request": request,
        "intent": detected["intent"],
        "confidence": detected["confidence"],
        "matched": detected["matched"],
    }
