from brain import session

def chat(message: str, session_id: str = "default"):
    from brain import dashboard
    from core import decision

    session.add(session_id, "user", message)

    data = dashboard.build()
    q = (message or "").lower()

    intent = "general"
    answer = ""
    actions = []

    if "proxmox" in q and ("update" in q or "actualiz" in q or "sigur" in q):
        intent = "decision_proxmox_update"

        d = decision.decide("proxmox.update", {
            "truenas": "healthy",
            "critical_incidents": data["health"]["open_incidents"] > 0,
        })

        if d["allowed"]:
            answer = (
                f"Da, update-ul Proxmox pare permis acum. "
                f"Riscul este {d['risk']}. "
                f"Health Score este {data['health']['score']}%. "
                f"Verifică recomandările active înainte de execuție."
            )
        else:
            answer = (
                f"Nu recomand update Proxmox acum. "
                f"Motiv: {', '.join(d.get('reasons', []))}"
            )

        actions.append({
            "title": "Create update task",
            "action": "task.create.proxmox_update",
            "requires_confirmation": True,
        })

    elif "opnsense" in q or "firewall" in q:
        intent = "provider_opnsense"

        opnsense = next(
            (p for p in data["providers"] if p["name"].lower() == "opnsense"),
            None
        )

        if opnsense:
            answer = (
                f"OPNsense este în starea: {opnsense['status']}. "
                f"Detalii: {opnsense['primary']}, {opnsense['secondary']}. "
            )

            if opnsense["status"] == "warning":
                answer += (
                    "Există o recomandare activă: planifică reboot într-o fereastră de mentenanță."
                )

            actions.append({
                "title": "Explain OPNsense impact",
                "action": "impact.opnsense",
                "requires_confirmation": False,
            })
        else:
            answer = "Nu am găsit date despre OPNsense."

    elif "health" in q or "score" in q or "scor" in q:
        intent = "explain_health"
        h = data["health"]

        answer = (
            f"Health Score este {h['score']}% și statusul este {h['status']}. "
            f"Sunt {h['open_incidents']} incidente deschise. "
        )

        if data["recommendations"]:
            top = data["recommendations"][0]
            answer += (
                f"Recomandarea principală este pentru {top['provider']}: "
                f"{top['recommendation']}"
            )
        else:
            answer += "Nu există recomandări importante acum."

    elif "docker" in q:
        intent = "provider_docker"

        docker = next(
            (p for p in data["providers"] if p["name"].lower() == "docker"),
            None
        )

        if docker:
            answer = (
                f"Docker este {docker['status']}: "
                f"{docker['primary']}, {docker['secondary']}."
            )
        else:
            answer = "Nu am găsit date despre Docker."

    else:
        intent = "summary"
        h = data["health"]

        answer = (
            f"Homelab-ul are Health Score {h['score']}% ({h['status']}). "
            f"Sunt {len(data['providers'])} provideri monitorizați, "
            f"{len(data['tasks'])} task-uri recente și "
            f"{len(data['recommendations'])} recomandări active."
        )

    session.add(session_id, "assistant", answer)

    return {
        "mode": "copilot_chat_v1",
        "intent": intent,
        "confidence": 0.9,
        "answer": answer,
        "context_used": [
            "dashboard",
            "recommendations",
            "tasks",
            "providers",
            "session",
        ],
        "actions": actions,
        "history": session.history(session_id),
    }
