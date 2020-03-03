from Seq0 import *

FOLDER = "../Session-04/"
list_genes = ["U5", "ADA", "FRAT1", "FXN"]

for gene in list_genes:
    print("Gene", gene, "---> Length:", seq_len(seq_read_fasta(FOLDER+gene+".txt")))

