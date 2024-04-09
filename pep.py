from flask import Flask, request, jsonify
from functools import wraps
import requests

app = Flask(__name__)

# 使用者帳號和密碼 (簡化示例,實際應用中應更安全) 
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
    
    # 解析請求數據,提取相關信息
    service_id = int.from_bytes(request_data[0:4], byteorder="big")
    method_id = int.from_bytes(request_data[12:14], byteorder="big") 
    client_id = int.from_bytes(request_data[14:18], byteorder="big")
    
    # 構造授權請求
    auth_request = {
        "service_id": service_id,
        "method_id": method_id,
        "client_id": client_id
    }
    
    # 將授權請求轉發到PDP進行決策
    decision = pdp_request(auth_request)
    
    if decision == "allow":
        return jsonify({"decision": decision})  
    else:
        return jsonify({"decision": decision}), 403

def pdp_request(auth_request):
    url = "http://100.77.173.105:5001/pdp"
    headers = {"Content-Type": "application/octet-stream"}
    response = requests.post(url, json=auth_request, headers=headers)
    return response.json()["decision"]

if __name__ == '__main__':
    app.run(host='100.77.173.105', port=5000, debug=True)