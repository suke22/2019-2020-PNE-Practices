class Seq:
    """A class for representing sequences"""
    def __init__(self, strbases):
        # Initialize the sequence with the value
        # passed as argument when creating the object
        bases = ['A', 'C', 'G', 'T']
        for character in strbases:
            if character not in bases:
                print("Error!")
                self.strbases = "Error"
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
        """Calculate the length of the sequence"""
        return len(self.strbases)

    pass

def print_seqs(sequences):
    for element in sequences:
        print(f"Sequence {sequences.index(element)}: (Length: {element.len()}) {element}")

seq_list = [Seq("ACT"), Seq("GATA"), Seq("CAGATA")]

print_seqs(seq_list)

