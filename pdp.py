from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Policy Decision Point (PDP)
@app.route('/pdp', methods=['POST'])
def pdp_request():
    request_data = request.data
    decision = policy_engine_request(request_data)
    return jsonify({"decision": decision})

def policy_engine_request(request_data):
    url = "http://100.77.173.105:5002/policy-engine"
    headers = {"Content-Type": "application/octet-stream"}
    response = requests.post(url, data=request_data, headers=headers)
    return response.json()["decision"]

if __name__ == '__main__':
    app.run(port=5001, debug=True)
