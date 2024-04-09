import socket

# 建立一個UDP服務器物件
udpServer = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# 設定服務器的IP地址和端口號
host = "100.77.173.105"
port = 30490
serverAddr = (host, port)

# 將服務器物件綁定到指定的地址
udpServer.bind(serverAddr)

# 定義一個函數,用於將四個字節的二進制數轉換為十進制數,並返回整數
def bytes_to_int(bytes):
    return int.from_bytes(bytes, byteorder="big")

# 定義一個函數,用於解析SOME/IP訊息的各個字段,並返回一個字典
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
    return someip_msg

# 使用while迴圈,不斷地接收客戶端發送的訂閱請求
while True:
    data, clientAddr = udpServer.recvfrom(1024)
    someip_msg = parse_someip_msg(data)
    print(f"收到來自{clientAddr}的SOME/IP-SD Subscribe訊息")
    print(f"服務ID: {someip_msg['service_id']}, 方法ID: {someip_msg['method_id']}")

# 關閉服務器物件
udpServer.close()