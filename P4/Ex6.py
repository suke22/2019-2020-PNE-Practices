import socket
import termcolor
from pathlib import Path

IP = "127.0.0.1"
PORT = 8080

def get_resource(path):
    cod = 200

    if path == "/":
        resp = Path("index.html").read_text()
    elif path == "/info/A":
        resp = Path("A.html").read_text()
    elif path == "/info/C":
        resp = Path("C.html").read_text()
    elif path == "/info/G":
        resp = Path("G.html").read_text()
    elif path == "/info/T":
        resp = Path("T.html").read_text()
    else:
        resp = Path("Error.html").read_text()
        cod = 404
    return resp, cod

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
    print(f"Method: {method}")
    body = ""
    code = 0

    if method == "GET":
        path = words[1]
        print(f"Path: {path}")
        body, code = get_resource(path)

    if code == 200:
        status_str = "OK"
    else:
        status_str = "Not Found"
    status_line = f"HTTP/1.1 {code} {status_str}\n"
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