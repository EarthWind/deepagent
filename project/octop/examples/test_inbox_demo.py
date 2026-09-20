import unittest

from inbox_demo import FakeRuntime, Inbox


class InboxSemantics(unittest.IsolatedAsyncioTestCase):
    async def test_submit_returns_before_execution_and_worker_is_serial(self):
        runtime = FakeRuntime()
        inbox = Inbox(runtime)
        inbox.submit("parent", "research", "t1", "one")
        inbox.submit("parent", "review", "t2", "two")
        self.assertEqual(runtime.calls, [])
        await inbox.drain()
        self.assertEqual([a for a, _ in runtime.calls], ["research", "parent", "review", "parent"])
        self.assertEqual(runtime.max_active, 1)
        self.assertEqual(inbox.pending, {})

    async def test_reply_uses_original_parent_thread(self):
        runtime = FakeRuntime()
        inbox = Inbox(runtime)
        inbox.submit("parent", "expert", "original-thread", "question")
        await inbox.drain()
        self.assertEqual(runtime.calls[-1], ("parent", "original-thread"))
        self.assertEqual(inbox.notifications[0]["thread"], "original-thread")
        self.assertIn("original-thread", runtime.history)

    async def test_target_failure_still_gets_parent_synthesis_and_failure_notice(self):
        runtime = FakeRuntime()
        inbox = Inbox(runtime)
        inbox.submit("parent", "failing-expert", "t", "question")
        await inbox.drain()
        self.assertEqual(runtime.calls[-1], ("parent", "t"))
        self.assertEqual(inbox.notifications[0]["status"], "failed")
        self.assertIn("模拟专家失败", inbox.notifications[0]["text"])

    async def test_new_inbox_has_no_recovered_pending_job(self):
        runtime = FakeRuntime()
        before = Inbox(runtime)
        before.submit("parent", "expert", "t", "question")
        after = Inbox(runtime)
        self.assertEqual(len(before.pending), 1)
        self.assertEqual(after.pending, {})
        self.assertTrue(after.queue.empty())


if __name__ == "__main__":
    unittest.main()
