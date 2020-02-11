dna = input("Introduce the sequence:" )

counta = 0
countc = 0
countt = 0
countg = 0

for character in dna:
    if character == "A":
        counta += 1
    elif character == "C":
        countc += 1
    elif character == "T":
        countt += 1
    elif character == "G":
        countg += 1
print("Total length: ", len(dna))
print("A: ", counta)
print("C: ", countc)
print("G: ", countg)
print("T: ", countt)
