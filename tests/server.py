import socket
import time

# 建立一個UDP服務器物件
udpServer = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# 設定服務器的IP地址和端口號
host = "100.77.173.105"
port = 1000
serverAddr = (host, port)

# 將服務器物件綁定到指定的地址
udpServer.bind(serverAddr)

# 定義一個函數，用於將四個字節的二進制數轉換為十進制數，並返回整數
def bytes_to_int(bytes):
    return int.from_bytes(bytes, byteorder="big")

# 定義一個函數，用於解析SOME/IP訊息的各個字段，並返回一個字典
def parse_someip_msg(data):
    someip_msg = {}
    someip_msg["service_id"] = bytes_to_int(data[0:4])
    someip_msg["method_id"] = bytes_to_int(data[4:8])
    someip_msg["client_id"] = bytes_to_int(data[8:12])
    someip_msg["session_id"] = bytes_to_int(data[12:16])
    someip_msg["msg_length"] = bytes_to_int(data[16:20])
    someip_msg["msg_type"] = data[20]
    someip_msg["msg_version"] = data[21]
    someip_msg["msg_return_code"] = data[22]
    someip_msg["payload"] = data[23:]
    return someip_msg

# 定義一個函數，用於解析負載字節串的各個字段，並返回一個字典
def parse_payload(payload):
    payload_data = {}
    payload_data["payload_length"] = payload[0]
    payload_data["payload_type"] = payload[1]
    payload_data["payload_value"] = payload[2]
    return payload_data

# 定義一個函數，用於執行油門或煞車訊號對應的動作，並打印出結果
def execute_signal(payload_type, payload_value):
    if payload_type == 0x01:
        throttle_opening = payload_value / 100
        print(f"油門開度為 {throttle_opening}")
        speed = throttle_opening * 100
        print(f"車速為 {speed} km/h")
    elif payload_type == 0x02:
        brake_force = payload_value / 100
        print(f"煞車力度為 {brake_force}")
        deceleration = brake_force * 10
        print(f"減速度為 {deceleration} m/s^2")
    else:
        print("負載類型錯誤")

# 使用while迴圈，不斷地接收客戶端發送的訊號
while True:
    data, clientAddr = udpServer.recvfrom(1024)
    someip_msg = parse_someip_msg(data)
    payload_data = parse_payload(someip_msg["payload"])
    execute_signal(payload_data["payload_type"], payload_data["payload_value"])
    time.sleep(1)
