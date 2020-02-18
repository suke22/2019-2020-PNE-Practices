from pathlib import Path


def seq_ping():
    print("OK!")


def seq_read_fasta(filename):
    file_contents = Path(filename).read_text()
    seq_dna = file_contents
    index_start = seq_dna.find("\n")
    seq_dna = seq_dna[index_start:]
    seq_dna = seq_dna.replace("\n", "")
    return seq_dna[0:20]


def seq_len(filename):
    file_contents = Path(filename).read_text()
    seq_dna = file_contents
    index_start = seq_dna.find("\n")
    seq_dna = seq_dna[index_start:]
    seq_dna = seq_dna.replace("\n", "")
    return len(seq_dna)