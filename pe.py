from flask import Flask, request, jsonify

app = Flask(__name__)

# 策略函數
def malicious_signal_policy(request_data):
    someip_msg = parse_someip_msg(request_data)
    if someip_msg.get("payload")[2] == 100:
        return False
    return True

def traffic_info_policy(request_data):
    someip_msg = parse_someip_msg(request_data)
    return True

def vehicle_control_policy(request_data):
    someip_msg = parse_someip_msg(request_data)
    return True

def risk_policy(request_data):
    someip_msg = parse_someip_msg(request_data)
    return True

# 策略列表
policies = [
    malicious_signal_policy,
    traffic_info_policy,
    vehicle_control_policy,
    risk_policy
]

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

# 評估請求
def evaluate_request(request_data):
    for policy in policies:
        if not policy(request_data):
            return False
    return True

@app.route('/evaluate-policies', methods=['POST'])
def evaluate_policies():
    request_data = request.data
    decision = "allow" if evaluate_request(request_data) else "deny"
    return jsonify({"decision": decision})

if __name__ == '__main__':
    app.run(host='100.77.173.105', port=5002, debug=True)
