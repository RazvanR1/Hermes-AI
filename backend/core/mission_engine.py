from planner_v2.planner import build_goal


class MissionEngine:

    def execute(self, mission: str):

        plan = build_goal(mission)

        if not plan.get("ok"):
            return plan

        return {
            "mission": mission,
            "planner": "planner_v2",
            "plan": plan,
            "approval_required": True,
            "status": "waiting_approval",
        }


mission_engine = MissionEngine()
