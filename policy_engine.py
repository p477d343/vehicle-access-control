from flask import Flask, request, jsonify

app = Flask(__name__)

# Policy Engine
@app.route('/policy-engine', methods=['POST'])
def policy_engine_request():
    request_data = request.data
    someip_msg = parse_someip_msg(request_data)
    decision = evaluate_request(someip_msg)
    return jsonify({"decision": "allow" if decision else "deny"})

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
    return someip_msg

# 策略函數
def malicious_signal_policy(someip_msg):
    if someip_msg.get("payload")[2] == 100:
        return False
    return True

def traffic_info_policy(someip_msg):
    return True

def vehicle_control_policy(someip_msg):
    return True

def risk_policy(someip_msg):
    return True

# 評估請求
def evaluate_request(someip_msg):
    policies = [
        malicious_signal_policy,
        traffic_info_policy,
        vehicle_control_policy,
        risk_policy
    ]
    for policy in policies:
        if not policy(someip_msg):
            return False
    return True

if __name__ == '__main__':
    app.run(host='100.77.173.105', port=5002, debug=True)
