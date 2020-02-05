def fibonacci(n):
    if n < 0:
        print("Incorrect input")
    elif n == 1:
        return 0
    else:
        return fibonacci(n - 2) + fibonacci(n - 1)


print("5th Fibonacci term: ", fibonacci(5))
print("10th Fibonacci term: ", fibonacci(10))
print("15th Fibonacci term: ", fibonacci(15))
