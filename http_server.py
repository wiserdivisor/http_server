import socket

HOST = "127.0.0.1"
PORT = 8080

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)         # CREATE SOCKET
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # SET OPTIONS
server_socket.bind((HOST,PORT))                                           # BIND
server_socket.listen(5)                                                   # LISTEN

print(f"Listening on http://{HOST}:{PORT}/")

while True:
    conn, addr = server_socket.accept()
    print(f"Connected from {addr}")

    request_data = b""
    while b"\r\n\r\n" not in request_data:
        chunk = conn.recv(4096)
        if not chunk:
            break
        request_data += chunk

    print("\n---- Raw Request ----")
    print(request_data.decode(errors="encode"))

    conn.close()