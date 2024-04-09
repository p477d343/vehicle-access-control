import socket
import requests
from requests.auth import HTTPBasicAuth
import json

# 定義一些常數,用於表示SOME/IP訊息的服務ID,方法ID,客戶端ID,會話ID
SERVICE_ID = 0x1234
METHOD_ID = 0x0001
CLIENT_ID = 0x0001
SESSION_ID = 0x0001

# 建立一個UDP客戶端物件
udpClient = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# 設定服務器的IP地址和端口號
host = "100.77.173.105" 
port = 30490
serverAddr = (host, port)

# 設定PEP的URL和認證憑證
pep_url = "http://100.77.173.105:5000/access-request"
auth = HTTPBasicAuth("admin", "password")

# 生成一個SOME/IP-SD Subscribe訊息
msg_length = 8
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
)

# 發送訂閱請求到PEP進行存取控制 
headers = {'Content-Type': 'application/octet-stream'}
response = requests.post(pep_url, data=someip_msg, headers=headers, auth=auth)
print("PEP response:", response.json())

if response.status_code == 200 and response.json()["decision"] == "allow":
    # 如果允許訪問,則發送訂閱請求到SOME/IP服務器
    udpClient.sendto(someip_msg, serverAddr) 
    print("已發送SOME/IP-SD Subscribe訊息")
else:
    print("訂閱請求被拒絕")

# 關閉客戶端物件
udpClient.close()