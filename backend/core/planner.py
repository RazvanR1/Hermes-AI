from typing import Dict, Any, List

def build(task: str, ctx: Dict[str, Any]) -> Dict[str, Any]:

    task_lower = task.lower()

    steps: List[dict] = []

    if "proxmox" in task_lower and ("update" in task_lower or "actualiz" in task_lower):

        steps = [
            {
                "step": 1,
                "title": "Check backups",
                "status": "pending",
                "action": "backup.verify"
            },
            {
                "step": 2,
                "title": "Check TrueNAS",
                "status": "pending",
                "action": "storage.verify"
            },
            {
                "step": 3,
                "title": "Check OPNsense",
                "status": "pending",
                "action": "opnsense.verify"
            },
            {
                "step": 4,
                "title": "Check running containers",
                "status": "pending",
                "action": "docker.verify"
            },
            {
                "step": 5,
                "title": "Run update",
                "status": "pending",
                "action": "proxmox.update"
            },
            {
                "step": 6,
                "title": "Verify services",
                "status": "pending",
                "action": "guardian.verify"
            }
            ]

    else:

        steps = [
            {
                "step":1,
                "title":"Analyze task",
                "status":"pending",
                "action":"analysis"
            },
            {
                "step":2,
                "title":"Execute",
                "status":"pending",
                "action":"execute"
            }
        ]

    return {

        "mode":"plan_v1",

        "task":task,

        "steps":steps,

        "estimated_duration":len(steps)*2

    }
