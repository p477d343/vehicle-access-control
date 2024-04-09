from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Policy Decision Point (PDP)
@app.route('/pdp', methods=['POST'])
def pdp_request():
    auth_request = request.json
    decision = policy_engine_request(auth_request)
    return jsonify({"decision": decision})

def policy_engine_request(auth_request):
    url = "http://100.77.173.105:5002/policy-engine"
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, json=auth_request, headers=headers)
    return response.json()["decision"]

if __name__ == '__main__':
    app.run(host='100.77.173.105', port=5001, debug=True)