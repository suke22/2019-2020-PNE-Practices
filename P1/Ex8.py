from Seq1 import Seq

# -- Create a Null sequence
s1 = Seq()

# -- Create a valid sequence
s2 = Seq("ACTGA")

# -- Create an invalid sequence
s3 = Seq("Invalid sequence")

for seq, value in enumerate([s1, s2, s3]):
    print(f"Sequence {seq}: (Length: {value.len()}) {value}\n Bases: {value.seq_count()} \n "
          f"Rev: {value.seq_reverse()} \n Comp: {value.seq_complement()}")