import unittest
from datetime import time
from policy_engine.engine import PolicyEngine
from policy_engine.policies import Policy, Decision

class TestPolicyEngine(unittest.TestCase):
    def setUp(self):
        self.policies = [
            Policy("Test Policy", ["TEST"], ["test"], ["LOW"], [time(0, 0), time(23, 59)], Decision.PERMIT)
        ]
        self.engine = PolicyEngine()
        self.engine.policies = self.policies

    def test_make_decision(self):
        request = {
            "vehicle_id": "TEST",
            "action": "test"
        }
        decision = self.engine.make_decision(request)
        self.assertEqual(decision, Decision.PERMIT)

if __name__ == '__main__':
    unittest.main()