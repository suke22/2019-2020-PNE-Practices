from Seq1 import Seq

FOLDER = "../Session-04/"
EXT = ".txt"
GENES = ["U5", "ADA", "FRAT1", "FXN", "RNU6_269P"]
BASES = ['A', 'T', 'C', 'G']

for gene in GENES:
    s = Seq()
    s.read_fasta(FOLDER + gene + EXT)

    # -- Dictionary with the values
    d = s.seq_count()

    # -- Create a list with all the values
    ll = list(d.values())

    # -- Calculate the maximum
    m = max(ll)
    print(f"Gene {gene}: Most frequent Base: {BASES[ll.index(m)]}")

#no lo entiendo!!!!!!!!!!!!!!!!