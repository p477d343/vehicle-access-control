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

def get_service_policies(service_id):
    # 根據服務ID獲取相關策略，這裡使用虛擬策略
    policies = [
        "check_subscriber_authorization",
        "check_subscriber_history",
        "check_system_security_status"
    ]
    return policies

def is_authorized_subscriber(subscriber_id, service_id):
    # 檢查訂閱者是否為服務的授權用戶，這裡簡單地用ID判斷
    return subscriber_id != "ECUC"

def has_suspicious_history(subscriber_id):
    # 檢查訂閱者之前是否有可疑行為，這裡簡單地用ID判斷
    return subscriber_id == "ECUC"

def is_high_risk_environment():
    # 檢查當前系統安全狀態和威脅情報，這裡簡單地返回True
    return True

# 評估請求
def evaluate_request(someip_msg):
    subscriber_id = someip_msg["client_id"]
    service_id = someip_msg["service_id"]

    # 獲取服務相關的策略
    policies = get_service_policies(service_id)

    # 風險評估
    risk_score = 0

    # 檢查訂閱者身份和權限
    if not is_authorized_subscriber(subscriber_id, service_id):
        risk_score += 1

    # 檢查訂閱者之前的行為歷史
    if has_suspicious_history(subscriber_id):
        risk_score += 1

    # 考慮當前系統安全狀態和威脅情報
    if is_high_risk_environment():
        risk_score += 1

    # 根據風險評估結果做出決策
    if risk_score >= 2:
        return False
    else:
        return True

if __name__ == '__main__':
    app.run(host='localhost', port=5002, debug=True)