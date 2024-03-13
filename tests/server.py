from flask import Flask, request, jsonify
from functools import wraps
import socket

app = Flask(__name__)

# 使用者帳號和密碼（簡化示例，實際應用中應更安全）
users = {"admin": "password"}

# 策略列表
policies = []

# HTTP Basic Auth身份驗證裝飾器
def require_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or users.get(auth.username) != auth.password:
            return jsonify({"message": "Authentication failed"}), 403
        return f(*args, **kwargs)
    return decorated

# SOME/IP 訊息解析函數
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
    #print("\n someip_msg = "+ str(someip_msg) + "\n")
    return someip_msg

# 策略函數
def malicious_signal_policy(request_data):
    someip_msg = parse_someip_msg(request_data)
    print("\n someip_msg = " + str(someip_msg.get("payload")[2]))
    if someip_msg.get("payload")[2] == 100:
        return False
    return True

def traffic_info_policy(request_data):
    someip_msg = parse_someip_msg(request_data)
    #if someip_msg.get("service_id") == 0x0001 and someip_msg.get("method_id") == 0x0002 and someip_msg.get("payload")[1] == 0x01:
    #    return True
    #return False
    return True

def vehicle_control_policy(request_data):
    someip_msg = parse_someip_msg(request_data)
    #if someip_msg.get("service_id") == 0x0001 and someip_msg.get("method_id") == 0x0002 and someip_msg.get("payload")[1] == 0x02:
    #    return True
    #return False
    return True

def risk_policy(request_data):
    someip_msg = parse_someip_msg(request_data)
    #if someip_msg.get("payload")[2] > 80:
    #    return False
    return True

# 初始化策略
policies.append(malicious_signal_policy)
policies.append(traffic_info_policy)
policies.append(vehicle_control_policy)
policies.append(risk_policy)

# 評估請求
def evaluate_request(request_data):
    for policy in policies:
        if not policy(request_data):
            return False
    return True

# 存取請求API
@app.route('/access-request', methods=['POST'])
@require_auth
def access_request():
    request_data = request.data
    #print(request_data)
    decision = "allow" if evaluate_request(request_data) else "deny"
    return jsonify({"decision": decision})

if __name__ == '__main__':
    app.run(host='100.77.173.105', port=5000, debug=True)
