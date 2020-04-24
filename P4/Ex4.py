import socket
import termcolor
from pathlib import Path

IP = "127.0.0.1"
PORT = 8080

def get_resource(path):
    resp = ""
    if path == "/info/A":
        resp = Path("A.html").read_text()
    elif path == "/info/C":
        resp = Path("C.html").read_text()
    elif path == "/info/G":
        resp = Path("G.html").read_text()
    elif path == "/info/T":
        resp = Path("T.html").read_text()
    return resp

def process_client(s):
    req_raw = s.recv(2000)
    req = req_raw.decode()

    print("Message FROM CLIENT: ")
    lines = req.split('\n')
    req_line = lines[0]

    print("Request line: ", end="")
    termcolor.cprint(req_line, "green")
    words = req_line.split(' ')
    method = words[0]
    path = words[1]
    print(f"Method: {method}")
    print(f"Path: {path}")
    body = ""

    if method == "GET":
        body = get_resource(path)
    status_line = "HTTP/1.1 200 OK\n"
    header = "Content-Type: text/html\n"
    header += f"Content-Length: {len(body)}\n"
    response_msg = status_line + header + "\n" + body
    cs.send(response_msg.encode())

ls = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ls.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
ls.bind((IP, PORT))
ls.listen()

print("SEQ Server configured!")
while True:
    print("Waiting for clients....")
    try:
        (cs, client_ip_port) = ls.accept()
    except KeyboardInterrupt:
        print("Server Stopped!")
        ls.close()
        exit()
    else:
        process_client(cs)
        cs.close()