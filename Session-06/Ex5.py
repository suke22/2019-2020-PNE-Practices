from Client0 import Client
from Seq1 import Seq

IP = "127.0.0.1"
PORT = 8080

c = Client(IP, PORT)

print(c)

FOLDER = "../Session-04/"
FILENAME = "U5.txt"

sequence = Seq().read_fasta(FOLDER + FILENAME)

c.debug_talk("Sending the U5 Gene to the server...")
c.debug_talk(str(sequence))