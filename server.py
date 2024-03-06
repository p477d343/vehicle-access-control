import socket
import threading
from utils.config import SERVER_HOST, SERVER_PORT
from utils.logger import logger
from request_handler import handle_request

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((SERVER_HOST, SERVER_PORT))

def handle_client(conn, addr):
    try:
        logger.info(f'Accepted connection from {addr}')
        while True:
            data = conn.recv(1024)
            if not data:
                break
            response = handle_request(data)
            conn.sendall(response.encode('utf-8'))
    except Exception as e:
        logger.error(f'Error handling client {addr}: {e}')
    finally:
        conn.close()
        logger.info(f'Closed connection from {addr}')

def start_server():
    server_socket.listen(5)
    logger.info(f'Server listening on {SERVER_HOST}:{SERVER_PORT}')
    while True:
        conn, addr = server_socket.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

if __name__ == '__main__':
    start_server()