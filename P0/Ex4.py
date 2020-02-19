from Seq0 import *

FOLDER = "../Session-04/"
list = ["U5.txt", "ADA.txt", "FRAT1.txt", "FXN.txt"]
bases = ["A", "C", "G", "T"]
for text in list:
    print(text, ":")
    for element in bases:
        print("", element, ":", seq_count_base(seq_read_fasta(FOLDER+text), element))
    print("\n")