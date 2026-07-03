INTENTS = {
    "inventory": ["ce am", "inventar", "infrastructura", "infrastructură", "topologie", "componente"],
    "health": ["cum este", "status", "sanatate", "sănătate", "health", "homelab-ul meu", "serverul meu"],
    "incidents": ["incident", "incidente", "probleme deschise", "alarme", "warning", "ce probleme"],
    "memory": ["ce s-a schimbat", "istoric", "trend", "evenimente"],
    "actions": ["restart", "actualizeaza", "actualizează", "optimizeaza", "optimizează", "repara", "repară"],
}

def detect(text: str):
    q = (text or "").lower()
    best = {"intent": "health", "confidence": 0.3, "matched": []}

    for intent, words in INTENTS.items():
        matched = [w for w in words if w in q]
        if matched:
            score = min(0.99, 0.5 + 0.15 * len(matched))
            if score > best["confidence"]:
                best = {"intent": intent, "confidence": score, "matched": matched}

    return best
