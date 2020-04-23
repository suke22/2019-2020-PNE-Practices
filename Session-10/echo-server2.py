import socket
import termcolor

IP = "127.0.0.1"
PORT = 8080
num_con = 0

ls = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ls.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

ls.bind((IP, PORT))

ls.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

ls.listen()
print("Server is configured")

while True:
    print("Waiting for Clients to connect")

    try:
        (cs, client_ip_port) = ls.accept()
    except KeyboardInterrupt:
        print("Server stopped by the user")
        ls.close()
        exit()

    else:
        num_con = num_con + 1
        print(f"CONNECTIONS{num_con}. Client IP,PORT {client_ip_port}")
        print("A client has connected to the server!")

        msg_raw = cs.recv(2048)
        msg = msg_raw.decode()
        print(f"Received Message:", end="")
        termcolor.cprint(msg, "green")

        response = "ECHO: " + msg + "\n"
        cs.send(response.encode())
        cs.close()
