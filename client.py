import socket
import requests
from requests.auth import HTTPBasicAuth

# 定義一些常數，用於表示SOME/IP訊息的服務ID，方法ID，客戶端ID，會話ID
SERVICE_ID = 0x0001
METHOD_ID = 0x0002
CLIENT_ID = 0x0001
SESSION_ID = 0x0001

# 定義訊號序列
signal_sequence = [
    ("throttle", 30),
    ("throttle", 50),
    ("brake", 20),
    ("throttle", 70),
    ("brake", 40),
    ("throttle", 100),  # 惡意訊號
    ("throttle", 60),
    ("brake", 30),
    ("throttle", 40)
]

# 建立一個UDP客戶端物件
udpClient = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# 設定服務器的IP地址和端口號
host = "100.77.173.105"
port = 1000
serverAddr = (host, port)

# 設定 Flask 服務器的 URL 和認證憑證
flask_url = "http://100.77.173.105:5000/access-request"
auth = HTTPBasicAuth("admin", "password")

# 發送訊號
for signal_type, signal_value in signal_sequence:
    # 生成負載
    payload_length = 1
    if signal_type == "throttle":
        payload_type = 0x01
    elif signal_type == "brake":
        payload_type = 0x02
    else:
        continue
    payload_value = signal_value
    #print(payload_value)
    payload = bytes([payload_length, payload_type, payload_value])
    #print("\n payload = " + str(payload) + ", btyes of payload_value:" + str(bytes(payload_value)))
    # 生成 SOME/IP 訊息
    msg_length = 8 + len(payload)
    msg_type = 0x00
    msg_version = 0x01
    msg_return_code = 0x00
    someip_msg = (
        int.to_bytes(SERVICE_ID, 4, byteorder="big")
        + int.to_bytes(METHOD_ID, 4, byteorder="big")
        + int.to_bytes(CLIENT_ID, 4, byteorder="big")
        + int.to_bytes(SESSION_ID, 4, byteorder="big")
        + int.to_bytes(msg_length, 4, byteorder="big")
        + bytes([msg_type, msg_version, msg_return_code])
        + payload
    )

    # 發送請求到 Flask 服務器進行存取控制
    headers = {'Content-Type': 'application/octet-stream'}
    #print("\n")
    #print(someip_msg)
    response = requests.post(flask_url, data=someip_msg, headers=headers, auth=auth)
    if response.json()["decision"] == "allow":
        # 如果允許訪問，則發送訊號到 SOME/IP 服務器
        udpClient.sendto(someip_msg, serverAddr)
        print(f"已發送 {signal_type} 訊號，訊號值為 {signal_value}")
    else:
        print(f"被拒絕發送 {signal_type} 訊號，訊號值為 {signal_value}")

# 關閉客戶端物件
udpClient.close()
