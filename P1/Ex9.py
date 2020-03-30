from Seq1 import Seq

FOLDER = "../Session-04/"
FILENAME = "U5.txt"

# -- Create a Null sequence
s = Seq()

# -- Initialize the null seq with the given file in fasta format
s.read_fasta(FOLDER+FILENAME)

print(f"Sequence : (Length: {s.len()}) {s}\n Bases: {s.seq_count()} \n "
          f"Rev: {s.seq_reverse()} \n Comp: {s.seq_complement()}")