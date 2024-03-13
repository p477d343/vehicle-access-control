from flask import Flask, request, jsonify
from functools import wraps
import requests

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
    decision = pdp_request(request_data)
    if decision == "allow":
        return jsonify({"decision": decision})
    else:
        return jsonify({"decision": decision}), 403

def pdp_request(request_data):
    url = "http://100.77.173.105:5001/pdp"
    headers = {"Content-Type": "application/octet-stream"}
    response = requests.post(url, data=request_data, headers=headers)
    return response.json()["decision"]

if __name__ == '__main__':
    app.run(host='100.77.173.105', port=5000, debug=True)
