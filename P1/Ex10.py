from Seq1 import Seq

FOLDER = "../Session-04/"
EXT = ".txt"
GENES = ["U5", "ADA", "FRAT1", "FXN", "RNU6_269P"]
BASES = ['A', 'T', 'C', 'G']

for gene in GENES:
    s = Seq()
    s.read_fasta(FOLDER + gene + EXT)
    value = s.seq_count()
    value_list = list(value.values())
    maxim = max(value_list)
    print(f"Gene {gene}: Most frequent Base: {BASES[value_list.index(maxim)]}")
