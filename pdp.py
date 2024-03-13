from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

POLICY_ENGINE_URL = "http://100.77.173.105:5002/evaluate-policies"

@app.route('/access-decision', methods=['POST'])
def access_decision():
    request_data = request.data
    response = requests.post(POLICY_ENGINE_URL, data=request_data)
    decision = response.json()["decision"]
    return jsonify({"decision": decision})

if __name__ == '__main__':
    app.run(host='100.77.173.105', port=5001, debug=True)
