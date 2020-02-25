from Seq0 import *

FOLDER = "../Session-04/"
list_genes = ["U5", "ADA", "FRAT1", "FXN"]
bases = ["A", "C", "G", "T"]

for gene in list_genes:
    print("Gene", gene, ":", seq_count(seq_read_fasta(FOLDER+gene+".txt")))