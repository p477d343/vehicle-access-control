import socket
import struct
import time

# 建立UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# 設定服務的IP地址和端口號
server_address = ('100.64.128.11', 30509)

# 建立SOME/IP-SD訂閱請求
service_id = 0x1234
instance_id = 0x5678
major_version = 0x01
message_type = 0x00
return_code = 0x00
protocol_version = 0x01
interface_version = 0x01
message_id = 0x01
length = 0x08
entry_array = struct.pack('!IIH', service_id, instance_id, major_version)
subscribe_message = struct.pack('!BBBBBBHI', message_type, return_code, protocol_version, interface_version, message_id, length, 0x00, 0x00) + entry_array

while True:
    # 發送SOME/IP-SD訂閱請求
    sock.sendto(subscribe_message, server_address)
    print('Sent SOME/IP-SD Subscribe message to', server_address)

    try:
        # 接收SOME/IP-SD訂閱響應
        data, address = sock.recvfrom(1024)
        message_type, return_code = struct.unpack_from('!BB', data)

        if message_type == 0x40 and return_code == 0x00:
            print('Received SOME/IP-SD Subscribe Ack message from', address)
        elif message_type == 0x40 and return_code == 0x03:
            print('Received SOME/IP-SD Subscribe Nack message from', address)
        else:
            print('Received unknown message from', address)

    except socket.timeout:
        print('Timeout waiting for response')

    time.sleep(1)