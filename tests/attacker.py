import socket
import requests
from requests.auth import HTTPBasicAuth
import time

# 定義一些常數,用於表示SOME/IP訊息的服務ID,方法ID,客戶端ID,會話ID
SERVICE_ID_UNAUTHORIZED = 0x5678  # 非法訂閱的服務ID
SERVICE_ID_AUTHORIZED = 0x1234  # 合法訂閱的服務ID
METHOD_ID = 0x0001
CLIENT_ID = 0x0003  # ECUC的ID 
SESSION_ID = 0x0002

# 建立一個UDP客戶端物件
udpClient = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# 設定服務器的IP地址和端口號
host = "100.77.173.105"
port = 30490
serverAddr = (host, port)

# 設定PEP的URL和認證憑證
pep_url = "http://100.77.173.105:5000/access-request"
auth = HTTPBasicAuth("admin", "password")

# 定義一個函數,用於生成SOME/IP-SD Subscribe訊息
def generate_someip_msg(service_id):
    msg_length = 8
    msg_type = 0x00
    msg_version = 0x01
    msg_return_code = 0x00
    someip_msg = (
        int.to_bytes(service_id, 4, byteorder="big")
        + int.to_bytes(METHOD_ID, 4, byteorder="big")
        + int.to_bytes(CLIENT_ID, 4, byteorder="big")
        + int.to_bytes(SESSION_ID, 4, byteorder="big")
        + int.to_bytes(msg_length, 4, byteorder="big")
        + bytes([msg_type, msg_version, msg_return_code])
    )
    return someip_msg

# 定義一個函數,用於發送訂閱請求到PEP進行存取控制
def send_subscribe_request(someip_msg):
    headers = {'Content-Type': 'application/octet-stream'}
    response = requests.post(pep_url, data=someip_msg, headers=headers, auth=auth)
    print("PEP response:", response.json())
    
    if response.status_code == 200 and response.json()["decision"] == "allow":
        # 如果允許訪問,則發送訂閱請求到SOME/IP服務器
        udpClient.sendto(someip_msg, serverAddr)
        print("已發送SOME/IP-SD Subscribe訊息")
    else:
        print("訂閱請求被拒絕")

# 發送多個訂閱請求,包括未授權的服務和頻繁的請求
print("發送未授權的服務訂閱請求...")
for i in range(5):
    unauthorized_msg = generate_someip_msg(SERVICE_ID_UNAUTHORIZED)
    send_subscribe_request(unauthorized_msg)
    time.sleep(0.5)  # 短暫等待,模擬頻繁請求

print("發送頻繁的服務訂閱請求...")
for i in range(10):
    authorized_msg = generate_someip_msg(SERVICE_ID_AUTHORIZED)
    send_subscribe_request(authorized_msg)
    time.sleep(0.1)  # 更短的等待時間,模擬高頻率請求

print("發送正常的服務訂閱請求...")
normal_msg = generate_someip_msg(SERVICE_ID_AUTHORIZED) 
send_subscribe_request(normal_msg)

# 關閉客戶端物件
udpClient.close()