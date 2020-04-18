from Client0 import Client
from Seq1 import Seq

IP = "127.0.0.1"
PORT1 = 8080
PORT2 = 8090

c1 = Client(IP, PORT1)
c2 = Client(IP, PORT2)

FOLDER = "../Session-04/"
FILENAME = "FRAT1.txt"

sequence = Seq().read_fasta(FOLDER + FILENAME)
base = str(sequence)
number = 10

print(f"Gene FRAT1: {base}")
c1.talk(f"Sending FRAT1 Gene to the server, in fragments of {number} bases")
c2.talk(f"Sending FRAT1 Gene to the server, in fragments of {number} bases")

for i in range(10):
    seq = base[(i)*number:(i+1)*number]
    print(f"Fragment {i+1}: {seq}")
    if i % 2:
        c2.talk(f"Fragment {i + 1}: {seq}")
    else:
        c1.talk(f"Fragment {i + 1}: {seq}")



