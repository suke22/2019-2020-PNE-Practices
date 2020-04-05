import socket

IP = "192.168.56.1"
PORT = 8088

# --- We create the socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# --- Establishing the connection with the server
s.connect((IP, PORT))

# --- Send  data to the server
s.send(str.encode("helloooo"))

# --- Receive data from the server
msg = s.recv(2000)

print("Message from the server:\n")
print(msg.decode("utf-8"))

# -- Closing the connection
s.close()