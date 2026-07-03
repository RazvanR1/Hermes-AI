from core import policy
from core import recommendations

def decide(action, ctx):
    result = {
        "mode": "decision_v1",
        "action": action,
        "allowed": True,
        "risk": "LOW",
        "reasons": [],
        "recommendations": [],
    }

    gate = policy.can_execute(action, ctx)

    if not gate["allowed"]:
        result["allowed"] = False
        result["risk"] = "HIGH"
        result["reasons"].append(gate["reason"])

    try:
        recs = recommendations.build(ctx)
        result["recommendations"] = recs.get("items", [])[:3]
    except Exception as e:
        result["reasons"].append(f"Recommendation engine error: {e}")

    return result
