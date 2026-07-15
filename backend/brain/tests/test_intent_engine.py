from __future__ import annotations

import unittest

from brain import (
    Action,
    RiskLevel,
    TargetType,
    brain,
    intent_engine,
)


class IntentEngineTests(unittest.TestCase):
    def test_restart_vm_in_romanian(self) -> None:
        intent = intent_engine.parse("repornește VM 110")

        self.assertEqual(intent.action, Action.RESTART)
        self.assertEqual(intent.target_type, TargetType.VM)
        self.assertEqual(intent.target_id, "110")
        self.assertEqual(intent.skill, "proxmox")
        self.assertTrue(intent.requires_confirmation)
        self.assertGreaterEqual(intent.confidence, 0.9)

    def test_status_vm_is_safe(self) -> None:
        context = brain.analyze("status VM110")

        self.assertEqual(context.intent.action, Action.STATUS)
        self.assertEqual(context.guardian.risk, RiskLevel.SAFE)
        self.assertFalse(context.guardian.requires_approval)
        self.assertTrue(context.guardian.allowed)
        self.assertEqual(len(context.plan.steps), 1)

    def test_restart_requires_approval(self) -> None:
        context = brain.analyze("restart VM110")

        self.assertEqual(context.guardian.risk, RiskLevel.MEDIUM)
        self.assertTrue(context.guardian.requires_approval)
        self.assertEqual(len(context.plan.steps), 3)

    def test_home_assistant_target(self) -> None:
        intent = intent_engine.parse("actualizează Home Assistant")

        self.assertEqual(intent.action, Action.UPDATE)
        self.assertEqual(
            intent.target_type,
            TargetType.HOME_ASSISTANT,
        )
        self.assertEqual(intent.skill, "homeassistant")

    def test_unknown_request_is_blocked(self) -> None:
        context = brain.analyze("fă ceva interesant")

        self.assertEqual(context.intent.action, Action.UNKNOWN)
        self.assertEqual(context.guardian.risk, RiskLevel.BLOCKED)
        self.assertFalse(context.guardian.allowed)


if __name__ == "__main__":
    unittest.main()
