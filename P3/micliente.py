from Client0 import Client

IP = "127.0.0.1"
PORT = 8080

c = Client(IP, PORT)
print(c)

print("*Testing PING")
print(c.talk("PING"))

print()
print("*Testing GET")
for i in range (5):
    cmd = f"GET {i}"
    print("GET", i, ":", c.talk(cmd))

print()
print("*Testing INFO")
info = c.talk("GET 0")
cmd = f"INFO {info}"
print(c.talk(cmd))

print()
print("*Testing COMP")
comp = c.talk("GET 0")
cmd = f"COMP {comp}"
print(cmd)
print(c.talk(cmd))

print()
print("*Testing REV")
rev = c.talk("GET 0")
cmd = f"REV {rev}"
print(cmd)
print(c.talk(cmd))

print()
print("*Testing GENE")
for i in ["U5", "ADA", "FRAT1", "FXN", "RNU6_269P"]:
    cmd = f"GENE {i}"
    print(cmd)
    print(c.talk(cmd))
    print()



