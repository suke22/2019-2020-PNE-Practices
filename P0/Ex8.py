from Seq0 import *

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

if