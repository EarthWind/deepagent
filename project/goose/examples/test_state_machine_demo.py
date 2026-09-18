"""Behavior tests for the teaching example; these do not test upstream Goose."""
import tempfile
import unittest
from pathlib import Path

from state_machine_demo import Effect, Machine, Store


class StateMachineTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.path = Path(self.temp.name) / "session.db"
        self.store = Store(self.path)
        self.store.apply((Effect("user", {"text": "one two three"}),))

    def tearDown(self):
        self.store.close()
        self.temp.cleanup()

    def wait_for_approval(self, machine=None):
        self.assertEqual((machine or Machine(self.store)).run(), "waiting_for_approval")
        return next(m.payload["call_id"] for m in self.store.load()
                    if m.kind == "approval_requested")

    def test_reconstruction_after_approval_wait_preserves_request(self):
        call_id = self.wait_for_approval()
        self.store.close()
        self.store = Store(self.path)
        self.store.answer(call_id, True)
        self.assertEqual(Machine(self.store).run(), "completed")
        results = [m for m in self.store.load() if m.kind == "tool_result"]
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].payload["output"], {"count": 3})

    def test_denial_does_not_execute_tool(self):
        calls = []
        machine = Machine(self.store, {"count_words": lambda args: calls.append(args)})
        call_id = self.wait_for_approval(machine)
        self.store.answer(call_id, False)
        self.assertEqual(machine.run(), "completed")
        self.assertEqual(calls, [])
        result = next(m for m in self.store.load() if m.kind == "tool_result")
        self.assertIn("denied", result.payload["output"]["error"])

    def test_repeated_resume_does_not_repeat_completed_call(self):
        calls = []
        def tool(args):
            calls.append(args)
            return {"count": 3}
        call_id = self.wait_for_approval()
        self.store.answer(call_id, True)
        for _ in range(2):
            self.assertEqual(Machine(self.store, {"count_words": tool}).run(), "completed")
        self.assertEqual(len(calls), 1)

    def test_repeated_wait_does_not_duplicate_approval_request(self):
        self.wait_for_approval()
        self.wait_for_approval()
        self.assertEqual(sum(m.kind == "approval_requested"
                             for m in self.store.load()), 1)

    def test_visibility_compaction_preserves_user_history(self):
        call_id = self.wait_for_approval()
        self.store.answer(call_id, True)
        Machine(self.store).run()
        before = [m.seq for m in self.store.load() if m.user_visible]
        self.store.compact_completed_turn("The answer was three.")
        messages = self.store.load()
        self.assertEqual([m.seq for m in messages if m.user_visible], before)
        self.assertEqual([m.kind for m in messages if m.agent_visible], ["summary"])

    def test_cancellation_before_tool_leaves_request_pending(self):
        call_id = self.wait_for_approval()
        self.store.answer(call_id, True)
        self.assertEqual(Machine(self.store, cancelled=lambda: True).run(), "cancelled")
        self.assertFalse(any(m.kind == "tool_result" for m in self.store.load()))
        self.assertEqual(Machine(self.store).run(), "completed")

    def test_tool_failure_is_recorded_as_observation(self):
        def broken(_):
            raise ValueError("bad input")
        call_id = self.wait_for_approval()
        self.store.answer(call_id, True)
        self.assertEqual(Machine(self.store, {"count_words": broken}).run(), "completed")
        result = next(m for m in self.store.load() if m.kind == "tool_result")
        self.assertEqual(result.payload["output"], {"error": "ValueError: bad input"})

    def test_duplicate_and_stale_approvals_are_rejected(self):
        call_id = self.wait_for_approval()
        self.store.answer(call_id, True)
        with self.assertRaises(ValueError):
            self.store.answer(call_id, False)
        Machine(self.store).run()
        self.store.apply((Effect("user", {"text": "next turn"}),))
        with self.assertRaises(ValueError):
            self.store.answer(call_id, True)


if __name__ == "__main__":
    unittest.main()
