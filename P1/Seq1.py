from pathlib import Path

class Seq:
    """A class for representing sequences"""
    NULL = "NULL"
    ERROR = "ERROR"
    def __init__(self, strbases=NULL):
        # Initialize the sequence with the value
        # passed as argument when creating the object
        bases = ['A', 'C', 'G', 'T']
        for character in strbases:
            if strbases == self.NULL:
                print("NULL Seq created")
                self.strbases = "NULL"
                return
            else:
                if character not in bases:
                    print("INVALID Seq!")
                    self.strbases = "ERROR"
                    return
                else:
                    print("New sequence created!")
                    self.strbases = strbases
                    return

    def __str__(self):
        """Method called when the object is being printed"""

        # -- We just return the string with the sequence
        return self.strbases

    def len(self):
        if self.strbases in (self.ERROR, self.NULL):
            return 0
        else:
            return len(self.strbases)

    def count_base(self, base):
        return self.strbases.count(base)

    def seq_count(self):
        d = {'A': self.count_base('A'), 'T': self.count_base('T'),
               'C': self.count_base('C'), 'G': self.count_base('G')}
        return d

    def seq_reverse(self):
        if self.strbases in (self.ERROR, self.NULL):
            return self.strbases
        else:
            return self.strbases[::-1]

    def seq_complement(self):
        self_comp = ""
        if self.strbases in (self.ERROR, self.NULL):
            return self.strbases
        else:
            for character in self.strbases:
                if character == "A":
                    self_comp = self_comp + "T"
                elif character == "C":
                    self_comp = self_comp + "G"
                elif character == "T":
                    self_comp = self_comp + "A"
                elif character == "G":
                    self_comp = self_comp + "C"
            return self_comp

    def read_fasta(self, filename):
        file_contents = Path(filename).read_text()
        index_start = file_contents.find("\n")
        seq_dna = file_contents[index_start:]
        seq_dna = seq_dna.split("\n")
        self.strbases= "".join(seq_dna)
        return self


    pass