from flask import Flask, request, jsonify
import time

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
    someip_msg["method_id"] = int.from_bytes(data[12:14], byteorder="big")
    someip_msg["client_id"] = int.from_bytes(data[14:18], byteorder="big")
    someip_msg["session_id"] = int.from_bytes(data[18:22], byteorder="big")
    someip_msg["msg_length"] = int.from_bytes(data[4:8], byteorder="big")
    someip_msg["msg_type"] = data[8]
    someip_msg["msg_version"] = data[9]
    someip_msg["msg_return_code"] = data[10]
    someip_msg["payload"] = data[22:]
    return someip_msg

client_history = {}

def calculate_risk_score(client_id, service_id):
    # 初始化風險值為0
    risk_score = 0
    
    # 檢查客戶端的歷史行為
    if client_id in client_history:
        # 如果客戶端之前曾經訂閱過未授權的服務,風險值增加20
        if "unauthorized_service" in client_history[client_id]:
            risk_score += 20
        
        # 如果客戶端在短時間內頻繁訂閱服務,風險值增加10
        if "frequent_requests" in client_history[client_id]:
            risk_score += 10
    
    # 檢查客戶端當前的訂閱請求
    if client_id == 0x0003 and service_id != 0x1234:
        # 如果ECUC嘗試訂閱非S1的服務,風險值增加50
        risk_score += 50
        
        # 將未授權的服務訂閱記錄到客戶端歷史中
        if client_id not in client_history:
            client_history[client_id] = []
        client_history[client_id].append("unauthorized_service")
    
    # 更新客戶端的訂閱請求歷史
    if client_id not in client_history:
        client_history[client_id] = []
    client_history[client_id].append(service_id)
    
    # 檢查客戶端的訂閱請求頻率
    if len(client_history[client_id]) > 10:
        # 如果客戶端在最近的10個請求中訂閱了過多的服務,視為頻繁請求
        client_history[client_id].append("frequent_requests")
    
    return risk_score


# 策略函數
def unauthorized_client_policy(someip_msg):
    client_id = someip_msg["client_id"]
    if client_id == 0x0003:  # ECUC的ID
        return False
    return True

def unauthorized_service_policy(someip_msg):
    client_id = someip_msg["client_id"] 
    service_id = someip_msg["service_id"]
    if client_id == 0x0003 and service_id != 0x1234:  # ECUC訂閱了非S1的服務
        return False
    return True

def malicious_signal_policy(someip_msg):
    if someip_msg.get("payload")[2] == 100:
        return False
    return True

def high_frequency_signal_risk(someip_msg):
    payload_type = someip_msg.get("payload")[1] 
    if payload_type == 0x01:  # 油門訊號
        global throttle_count, last_throttle_time
        current_time = time.time()
        if current_time - last_throttle_time <= 1:  # 1秒內再次收到油門訊號
            throttle_count += 1
        else:
            throttle_count = 1
        last_throttle_time = current_time
        
        if throttle_count > 5:  # 1秒內收到超過5次油門訊號,視為高風險
            return "high"
        elif throttle_count > 3:  # 1秒內收到超過3次油門訊號,視為中風險 
            return "medium"
        else:
            return "low"
        
    return "low"  # 非油門訊號,風險等級低

# 評估請求
def evaluate_request(someip_msg):
    policies = [
        unauthorized_client_policy,
        unauthorized_service_policy,
        malicious_signal_policy
    ]
    for policy in policies:
        if not policy(someip_msg):
            return False
        
    client_id = someip_msg["client_id"]
    service_id = someip_msg["service_id"]
    
    # 計算風險值 
    risk_score = calculate_risk_score(client_id, service_id)
    
    if risk_score > 50:  # 風險值超過閾值,拒絕訪問
        return False
    
    return True

throttle_count = 0
last_throttle_time = 0

if __name__ == '__main__':
    app.run(host='100.77.173.105', port=5002, debug=True)