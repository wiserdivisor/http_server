import socket

host = "127.0.0.1"
port = 8080

server_socket = socket.socket(socket.af_inet, socket.sock_stream)         # create socket
server_socket.setsockopt(socket.sol_socket, socket.so_reuseaddr, 1) # set options
server_socket.bind((host,port))                                           # bind
server_socket.listen(5)                                                   # listen

print(f"listening on http://{host}:{port}/")

while true:
    conn, addr = server_socket.accept()
    print(f"connected from {addr}")

    request_data = b""
    while b"\r\n\r\n" not in request_data:
        chunk = conn.recv(4096)
        if not chunk:
            break
        request_data += chunk

    print("\n---- raw request ----")
    print(request_data.decode(errors="encode"))

    conn.close()
