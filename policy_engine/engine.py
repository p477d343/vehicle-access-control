from datetime import datetime
from .policies import policies, Decision
from data.cache import get_risk_data

class PolicyEngine:
    def __init__(self):
        self.policies = policies

    def make_decision(self, request):
        vehicle_id = request["vehicle_id"]
        action = request["action"]
        current_time = datetime.now().time()

        # 進行風險評估
        risk_level = get_risk_data(vehicle_id, action)

        # 根據時間、風險級別和策略做出決策
        for policy in self.policies:
            if policy.applies_to(vehicle_id, action, risk_level, current_time):
                return policy.make_decision()

        return Decision.DENY