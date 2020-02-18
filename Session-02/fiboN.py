def fibon(n):
    n1 = 0
    n2 = 1
    if n < 0:
        print("Incorrect input")
    elif n == 1:
        return 1
    else:
        for i in range(2, n):
            nth = n1 + n2
            n1 = n2
            n2 = nth
        return n2


print("5th Fibonacci term: ", fibon(5))
print("10th Fibonacci term: ", fibon(10))
print("15th Fibonacci term: ", fibon(15))
