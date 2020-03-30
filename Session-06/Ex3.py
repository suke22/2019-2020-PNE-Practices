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
        
def generate_seqs(pattern, number):
    list_seqs=[]
    for i in range(1, number + 1):
        list_seqs.append(Seq(pattern * i))
    return list_seqs

seq_list1 = generate_seqs("A", 3)
seq_list2 = generate_seqs("AC", 5)

print("List 1:")
print_seqs(seq_list1)

print()
print("List 2:")
print_seqs(seq_list2)