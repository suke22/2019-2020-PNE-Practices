from pathlib import Path
FILENAME = "RNU6_269P.txt"
file_contents = Path(FILENAME).read_text()
seq_dna = file_contents
index_start = seq_dna.find("\n")
seq_dna = seq_dna[:index_start]
print(seq_dna)
