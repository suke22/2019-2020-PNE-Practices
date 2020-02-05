def fibon(n):
    if n < 0:
        print("Incorrect input")
    elif n == 1:
        return 0
    else:
        return fibon(n - 2) + fibon(n - 1)


print("5th Fibonacci term: ", fibon(5))
print("10th Fibonacci term: ", fibon(10))
print("15th Fibonacci term: ", fibon(15))
