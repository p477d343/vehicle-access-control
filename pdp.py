from flask import Flask, request, jsonify
import requests
import json

app = Flask(__name__)

# Policy Decision Point (PDP)
@app.route('/pdp', methods=['POST'])
def pdp_request():
    request_data = request.data
    decision = policy_engine_request(request_data)
    return jsonify({"decision": decision})

def policy_engine_request(request_data):
    authorization_request = json.loads(request_data)
    subscriber_id = authorization_request["subscriber_id"]
    service_id = authorization_request["service_id"]

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
        return "deny"
    else:
        return "allow"

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

if __name__ == '__main__':
    app.run(host='localhost', port=5001, debug=True)