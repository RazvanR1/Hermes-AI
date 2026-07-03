from providers.operations import client
from providers.operations import alerts as alerts_mod
from providers.operations import planner
from providers.operations import decision
from providers.operations import summary
from providers.operations import trend
from providers.operations import reasoning


def safe(fn):
    try:
        return {"ok": True, "data": fn()}
    except Exception as e:
        return {"ok": False, "error": str(e)}


def build():
    dashboard_result = safe(client.dashboard)
    updates_result = safe(client.update_status)

    alerts = alerts_mod.collect(dashboard_result, updates_result)
    tasks = planner.plan(alerts)
    decision_result = decision.decide(alerts, tasks)
    summary_result = summary.build(decision_result)
    trend_result = trend.analyze()

    rendered_like = {
        "status": decision_result.get("status"),
        "score": decision_result.get("score"),
        "critical": decision_result.get("critical", []),
        "warnings": decision_result.get("warnings", []),
        "healthy": decision_result.get("healthy", []),
        "today": decision_result.get("today", []),
    }

    reasoning_result = reasoning.analyze(rendered_like)

    return {
        "summary": summary_result,
        "decision": decision_result,
        "trend": trend_result,
        "reasoning": reasoning_result,
        "raw": {
            "dashboard": dashboard_result,
            "updates": updates_result,
        },
    }
