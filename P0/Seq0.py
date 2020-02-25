from pathlib import Path


def seq_ping():
    print("OK!")


def seq_read_fasta(filename):
    file_contents = Path(filename).read_text()
    seq_dna = file_contents
    index_start = seq_dna.find("\n")
    seq_dna = seq_dna[index_start:]
    seq_dna = seq_dna.replace("\n", "")
    return seq_dna


def seq_len(filename):
    file_contents = Path(filename).read_text()
    seq_dna = file_contents
    index_start = seq_dna.find("\n")
    seq_dna = seq_dna[index_start:]
    seq_dna = seq_dna.replace("\n", "")
    return len(seq_dna)


def seq_count_base(seq, base):
    counta = 0
    for letter in seq:
        if letter != base:
            counta = counta
        else:
            counta += 1
    return counta


def seq_count(seq):
    d = {'A': 0, 'C': 0, 'T': 0, 'G': 0}
    bases = ["A", "C", "G", "T"]
    count = 0
    for letter in bases:
        for character in seq:
            if letter == character:
                count += 1
            else:
                count = count
            d[letter] = count
        count = 0
    return d

