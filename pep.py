from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

PDP_URL = "http://100.77.173.105:5001/access-decision"

@app.route('/access-request', methods=['POST'])
def access_request():
    request_data = request.data
    response = requests.post(PDP_URL, data=request_data)
    decision = response.json()["decision"]
    if decision == "allow":
        # 執行允許訪問的操作,例如將請求轉發到 server.py
        return jsonify({"message": "Access allowed"}), 200
    else:
        return jsonify({"message": "Access denied"}), 403

if __name__ == '__main__':
    app.run(host='100.77.173.105', port=5000, debug=True)
