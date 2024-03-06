from datetime import datetime, time
from enum import Enum

class Decision(Enum):
    PERMIT = 1
    DENY = 2

class Policy:
    def __init__(self, name, vehicles, actions, risk_levels, allowed_times, decision):
        self.name = name
        self.vehicles = vehicles
        self.actions = actions
        self.risk_levels = risk_levels
        self.allowed_times = allowed_times
        self.decision = decision

    def applies_to(self, vehicle_id, action, risk_level, current_time):
        if (vehicle_id in self.vehicles and
            action in self.actions and
            risk_level in self.risk_levels and
            current_time in self.allowed_times):
            return True
        return False

    def make_decision(self):
        return self.decision

# 配置範例策略
policies = [
    Policy("允許低風險車輛遠程鎖車", ["ABC123", "DEF456"], ["lock"], ["LOW"], [time(0, 0), time(23, 59)], Decision.PERMIT),
    Policy("拒絕高風險車輛任何操作", ["XYZ789"], ["*"], ["HIGH"], [time(0, 0), time(23, 59)], Decision.DENY),
    Policy("允許測試車輛一切操作", ["TEST00"], ["*"], ["LOW", "MEDIUM", "HIGH"], [time(0, 0), time(23, 59)], Decision.PERMIT)
]