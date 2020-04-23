from Client0 import Client

PORT = 8080
IP = "127.0.0.1"

for i in range(5):
    c = Client(IP, PORT)
    c.debug_talk(f"Message{i}...")
