def build(task: str):
    q = (task or "").lower()

    plan = []

    if "update" in q or "actualiz" in q:

        plan.extend([
            {
                "step": 1,
                "action": "guardian.status",
                "description": "Verific starea generală"
            },
            {
                "step": 2,
                "action": "incidents.open",
                "description": "Verific incidentele"
            },
            {
                "step": 3,
                "action": "policy.check",
                "description": "Verific politicile"
            },
            {
                "step": 4,
                "action": "decision.proxmox.update",
                "description": "Calculez dacă update-ul este sigur"
            }
        ])

    elif "repar" in q or "repair" in q:

        plan.extend([
            {
                "step": 1,
                "action": "guardian.status",
                "description": "Analizez sistemul"
            },
            {
                "step": 2,
                "action": "recommendations.build",
                "description": "Generez recomandări"
            },
            {
                "step": 3,
                "action": "autoheal.run",
                "description": "Aplic auto-heal unde este permis"
            }
        ])

    else:

        plan.append({
            "step": 1,
            "action": "brain.answer",
            "description": "Răspuns standard"
        })

    return {
        "mode": "task_plan_v1",
        "task": task,
        "steps": plan,
    }
