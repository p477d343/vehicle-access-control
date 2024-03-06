import json
import re
from utils.logger import logger
from utils.auth import validate_token
from policy_engine.engine import PolicyEngine

engine = PolicyEngine()

def validate_request(request):
    # 驗證請求格式
    if not isinstance(request, dict):
        return False

    # 驗證必需欄位
    required_fields = ['vehicle_id', 'action']
    if not all(field in request for field in required_fields):
        return False

    # 驗證車輛ID格式
    vehicle_id = request['vehicle_id']
    if not re.match(r'^[A-Z0-9]{6}$', vehicle_id):
        return False

    return True

def handle_request(request_data):
    try:
        request = json.loads(request_data)
    except json.JSONDecodeError:
        return json.dumps({"error": "Invalid request format"})

    # 驗證請求
    if not validate_request(request):
        return json.dumps({"error": "Invalid request"})

    # 驗證身份
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return json.dumps({"error": "Missing authentication token"}), 401

    token = auth_header.split(' ')[1]
    vehicle_id = validate_token(token)
    if not vehicle_id:
        return json.dumps({"error": "Invalid authentication token"}), 401

    # 確認車輛ID一致
    if vehicle_id != request['vehicle_id']:
        return json.dumps({"error": "Vehicle ID mismatch"}), 403

    # 呼叫策略引擎做出決策
    decision = engine.make_decision(request)

    # 根據決策結果回應
    if decision == Decision.PERMIT:
        return json.dumps({"result": "Access granted"})
    else:
        return json.dumps({"error": "Access denied"})