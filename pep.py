from flask import Flask, request, jsonify
from functools import wraps
import requests
import json

app = Flask(__name__)

# 使用者帳號和密碼（簡化示例，實際應用中應更安全）
users = {"admin": "password"}

# HTTP Basic Auth身份驗證裝飾器
def require_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or users.get(auth.username) != auth.password:
            return jsonify({"message": "Authentication failed"}), 403
        return f(*args, **kwargs)
    return decorated

# Policy Enforcement Point (PEP)
@app.route('/access-request', methods=['POST'])
@require_auth
def access_request():
    request_data = request.data
    decision = evaluate_request(request_data)
    if decision == "allow":
        return jsonify({"decision": decision})
    else:
        return jsonify({"decision": decision}), 403

def parse_someip_msg(data):
    someip_msg = {}
    someip_msg["service_id"] = int.from_bytes(data[0:4], byteorder="big")
    someip_msg["method_id"] = int.from_bytes(data[4:8], byteorder="big")
    someip_msg["client_id"] = int.from_bytes(data[8:12], byteorder="big")
    someip_msg["session_id"] = int.from_bytes(data[12:16], byteorder="big")
    someip_msg["msg_length"] = int.from_bytes(data[16:20], byteorder="big")
    someip_msg["msg_type"] = data[20]
    someip_msg["msg_version"] = data[21]
    someip_msg["msg_return_code"] = data[22]
    someip_msg["payload"] = data[23:]
    return someip_msg

def get_service_provider(service_id):
    # 根據服務ID獲取服務提供者的ID，這裡簡單地返回ECUA
    return "ECUA"

def evaluate_request(request_data):
    someip_msg = parse_someip_msg(request_data)
    subscriber_id = someip_msg["client_id"]
    service_id = someip_msg["service_id"]
    provider_id = get_service_provider(service_id)

    # 封裝授權請求
    authorization_request = {
        "subscriber_id": subscriber_id,
        "service_id": service_id,
        "provider_id": provider_id
    }

    # 發送授權請求到PDP
    decision = pdp_request(json.dumps(authorization_request))
    return decision

def pdp_request(request_data):
    url = "http://localhost:5001/pdp"
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, data=request_data, headers=headers)
    return response.json()["decision"]

if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)