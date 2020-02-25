from Seq0 import *

FOLDER = "../Session-04/"
list = ["U5", "ADA", "FRAT1", "FXN"]
bases = ["A", "C", "G", "T"]
for text in list:
    print("Gene", text, ":")
    for element in bases:
        print("", element, ":", seq_count_base(seq_read_fasta(FOLDER+text+".txt"), element))
    print("\n")
