import os
import time
from email.utils import formatdate
import socket
from datetime import datetime

host = "127.0.0.1"
port = 8080
root = os.path.abspath("www")

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)         # create socket
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # set options
server_socket.bind((host,port))                                           # bind
server_socket.listen(5)                                                   # listen

print(f"listening on http://{host}:{port}/")

while True:
    conn, addr = server_socket.accept()
    print(f"connected from {addr}")

    request_data = b""
    while b"\r\n\r\n" not in request_data:
        chunk = conn.recv(4096)
        if not chunk:
            break
        request_data += chunk

    request_text = request_data.decode("latin-1")
    print("\n---- raw request START ----")
    print(request_text)
    print("\n---- raw request END ----")
    lines = request_text.split("\r\n")
    request_line = lines[0]
    request_line_tokens = request_line.split(" ")
    if(len(request_line_tokens) < 3):
        response = "HTTP/1.0 400 Bad Request\r\n\r\n<h1>400 Bad Request</h1>"
        conn.sendall(response.encode("latin-1"))
        conn.close()
        continue
    
    method = request_line_tokens[0]
    if(method not in ("GET", "POST", "HEAD")):
        body = b"<h1>501 Not Implemented.</h1>"
        status = "HTTP/1.0 501 Not Implemented\r\n"
   
    # FIND FILE USING URI AND RETURN ELSE 404 
    raw_uri = request_line_tokens[1]

    headers = {}
    for line in lines[1:]:
        if not line:
            break
        name, value = line.split(":",1)
        headers[name.strip().lower()] = value.strip()
    print(f"Method: {method}\r\nRaw URI: {raw_uri}\r\nHTTP Version: {http_version}")
    print("headers",headers)

    status_code = ""
    status_message = ""
    
    status_line = f"HTTP/1.0 {status_code} {status_message}\r\n"
    date_header = f"Date: {formatdate(timeval=time.time(), localtime=False, usegmt=True)}\r\n"
    server_header = "Server: VREDDYHTTP/1.0\r\n"

    

    body = b"<h1>Hello from VREDDY HTTP/1.0 Server.</h1><br><h1>This server is compliant with RFC-1945</h1>"
    content_type = "Content-Type: text/html; charset=utf-8\r\n"
    content_length = f"Content-Length: {len(body)}\r\n"

    headers_str = date_header + server_header + content_type + content_length + "\r\n"
    response = (status_line + headers_str).encode("utf-8") + body

    conn.sendall(response)
    conn.close()
