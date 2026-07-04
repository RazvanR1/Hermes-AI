from typing import Dict, Any, List


def explain(ctx: Dict[str, Any]) -> Dict[str, Any]:
    health = ctx.get("health", {})
    recommendations = ctx.get("recommendations", [])
    providers = ctx.get("providers", [])

    score = health.get("score", 0)
    status = health.get("status", "unknown")
    incidents = health.get("open_incidents", 0)

    reasons: List[str] = []

    if incidents:
        reasons.append(
            f"Există {incidents} incident(e) deschise."
        )

    opnsense = next(
        (p for p in providers if p.get("name") == "OPNsense"),
        None
    )

    if opnsense and opnsense.get("status") == "warning":
        reasons.append(
            "OPNsense necesită reboot."
        )

    estimated_score = score

    if opnsense and opnsense.get("status") == "warning":
        estimated_score += 8

    if incidents:
        estimated_score += min(incidents * 5, 10)

    estimated_score = min(100, estimated_score)

    explanation = (
        f"Health Score este {score}% ({status}). "
        + " ".join(reasons)
    )

    next_actions = [
        r["recommendation"]
        for r in recommendations
    ]

    return {
        "mode": "reasoning_v1",
        "score": score,
        "estimated_score": estimated_score,
        "explanation": explanation,
        "reasons": reasons,
        "next_actions": next_actions,
    }
