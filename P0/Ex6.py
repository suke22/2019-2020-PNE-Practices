from Seq0 import *

FOLDER = "../Session-04/"
filename = "U5.txt"

print("Gene U5:")
print("Frag:", seq_read_fasta(FOLDER+filename)[0:19])
sequence20 = seq_read_fasta(FOLDER+filename)[0:19]

print("Rev:", seq_reverse(sequence20))