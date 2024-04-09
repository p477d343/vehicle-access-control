import socket
import struct

# 創建UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# 綁定IP地址和端口號
server_address = ('100.64.128.11', 30509)
sock.bind(server_address)

print('Server started on', server_address)

while True:
    # 接收SOME/IP-SD訂閱請求
    data, address = sock.recvfrom(1024)
    message_type, return_code, protocol_version, interface_version, message_id, length = struct.unpack_from('!BBBBBB', data)

    if message_type == 0x00 and protocol_version == 0x01:
        service_id, instance_id, major_version = struct.unpack_from('!IIH', data, 8)
        print('Received SOME/IP-SD Subscribe message from', address)
        print('Service ID:', hex(service_id))
        print('Instance ID:', hex(instance_id))
        print('Major Version:', hex(major_version))

        # 發送SOME/IP-SD訂閱確認響應
        subscribe_ack_message = struct.pack('!BBBBBBHI', 0x40, 0x00, protocol_version, interface_version, message_id, length, 0x00, 0x00)
        sock.sendto(subscribe_ack_message, address)
        print('Sent SOME/IP-SD Subscribe Ack message to', address)