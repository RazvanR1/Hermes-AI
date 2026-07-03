from providers.operations import history


def analyze():
    stats = history.stats()
    latest = history.latest(10)

    predictions = []
    changes = []

    if stats.get("count", 0) < 2:
        return {
            "changes": [],
            "predictions": [],
            "note": "Istoricul este activ, dar sunt necesare cel puțin 2 snapshot-uri pentru trenduri.",
            "history": stats,
        }

    scores = [x.get("score") for x in latest if x.get("score") is not None]

    if len(scores) >= 2:
        current = scores[0]
        previous = scores[1]
        delta = current - previous

        if delta < 0:
            changes.append(f"Health score a scăzut cu {abs(delta)} puncte față de verificarea precedentă.")
        elif delta > 0:
            changes.append(f"Health score a crescut cu {delta} puncte față de verificarea precedentă.")
        else:
            changes.append("Health score este neschimbat față de verificarea precedentă.")

    if stats.get("min_score") is not None and stats.get("max_score") is not None:
        if stats["max_score"] - stats["min_score"] >= 15:
            predictions.append("Scorul variază semnificativ. Merită urmărite schimbările recente.")

    return {
        "changes": changes,
        "predictions": predictions,
        "history": stats,
    }
