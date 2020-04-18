from Client0 import Client
from Seq1 import Seq

IP = "127.0.0.1"
PORT = 8080

c = Client(IP, PORT)

FOLDER = "../Session-04/"
FILENAME = "U5.txt"

c.talk("Sending the U5 Gene to the server...")

sequence = Seq().read_fasta(FOLDER + FILENAME)
base = str(sequence)
number = 10
for i in range(5):
    seq = base[i*number:(i+1)*number]
    print(f"Fragment {i+1}: {seq}")
    c.talk(f"Fragment {i+1}: {seq}")

