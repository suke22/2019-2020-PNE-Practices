counta = 0
countc = 0
countt = 0
countg = 0

with open("dna.txt", "r") as f:
    for line in f:
        for character in line:
            if character == "A":
                counta += 1
            elif character == "C":
                countc += 1
            elif character == "T":
                countt += 1
            elif character == "G":
                countg += 1
    sumdna = counta + countc + countt + countg

print("Total length: ", sumdna)
print("A: ", counta)
print("C: ", countc)
print("G: ", countg)
print("T: ", countt)