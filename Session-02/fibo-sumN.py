def fibon(n):
    n1 = 0
    n2 = 1
    if n < 0:
        print("Incorrect input")
    elif n == 1:
        return 1
    else:
        count = 0
        sumn = 0
        while count < n:
            print(n1, end=" ")
            nth = n1 + n2
            n1 = n2
            n2 = nth
            count += 1
            sumn += n1
        return sumn


print("Sum of the first 5 terms of the Fibonacci series: ", fibon(5))
print("Sum of the first 10 terms of the Fibonacci series: ", fibon(10))

