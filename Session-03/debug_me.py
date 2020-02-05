def g(a, b):
    return a - b


def f(a, b, c, d):
    t0 = a + b - g(a, 0)
    t1 = g(c, d)
    try:
        t3 = 2 * (t0 / t1)
        return t0 + 2*t1 + t3*t3
    except ZeroDivisionError:
        return "The program does not work with zero division. Change the value of c and d"


print("Result 1: ", f(5, 2, 5, 0))
print("Result 2: ", f(0, 2, 3, 3))
print("Result 3: ", f(1, 3, 2, 3))
print("Result 4: ", f(1, 9, 22.0, 3))
