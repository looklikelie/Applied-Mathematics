from math import sin

from numpy import double


def func(x):
    return double(sin(x) * x ** 2)


def parabola(a, b, e):
    x1 = a
    x3 = b
    x2 = (b + a) / 2
    f1 = func(x1)
    f2 = func(x2)
    f3 = func(x3)
    iter_counter = 0
    func_counter = 3
    lengths = [b - a]
    while True:
        u = x2 - (((x2 - x1)**2) * (f2 - f3) - ((x2 - x3)**2) * (f2 - f1)) / (2 * (x2 - x1) * (f2 - f3) - (x2 - x3) *
                                                                              (f2 - f1))
        if abs(u - x2) < e and iter_counter > 0:
            return (u + x2) / 2, iter_counter, func_counter, lengths
        fu = func(u)
        if fu < f2:
            if u >= x2:
                x1 = x2
                f1 = f2
                x2 = u
                f2 = fu
            else:
                x3 = x2
                f3 = f2
                x2 = u
                f2 = fu
        elif fu > f2:
            if u >= x2:
                x3 = u
                f3 = fu
            else:
                x1 = u
                f1 = fu
        else:
            if u > x2:
                x1 = x2
                f1 = f2
                x3 = u
                f3 = fu
                x2 = (x1 + x3)/2
                f2 = func(x2)
                func_counter += 1
            else:
                x1 = u
                f1 = fu
                x3 = x2
                f3 = f2
                x2 = (x1 + x3) / 2
                f2 = func(x2)
                func_counter += 1
        lengths.append(x3 - x1)
        func_counter += 1
        iter_counter += 1


a, b, e = map(double, input().split())
print("======parabola======")
print("Eps = ", e)
minimum, iter_counter, func_counter, lengths = (parabola(a, b, e))
print("Minimum point is " + str(minimum) + "\nIteration number : " + str(iter_counter) + "\nFunction calculation "
                                                                                         "number : " + str(
    func_counter))
print("Values step by step :")
print(lengths)

for i in range (1, len(lengths)):
    print(lengths[i]/lengths[i-1])


