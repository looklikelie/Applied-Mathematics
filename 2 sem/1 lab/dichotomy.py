from math import sin

from numpy import double


def func(x):
    return double(sin(x) * x ** 2)


def dichotomy(a, b, e):
    d = (e / 2) * 0.9
    iter_counter = 0
    func_counter = 0
    lengths = [b-a]
    while b - a > e:
        x1 = (b + a) / 2 - d
        x2 = (b + a) / 2 + d
        if func(x1) < func(x2):
            b = x2
        else:
            a = x1
        iter_counter += 1
        func_counter += 2
        lengths.append(b - a)

    return (b + a) / 2, iter_counter, func_counter, lengths


a, b, e = map(double, input().split())
print("======dichotomy======")
print("Eps = ", e)
minimum, iter_counter, func_counter, lengths = (dichotomy(a, b, e))
print("Minimum point is " + str(minimum) + "\nIteration number : " + str(iter_counter) + "\nFunction calculation "
                                                                                         "number : " + str(
    func_counter))
print("Values step by step :")
print(lengths)

for i in range (1, len(lengths)):
    print(lengths[i]/lengths[i-1])



#3.1415926 6.2830 0.01
# 3.1415926 6.2830 0.0001
#3.1415926 6.2830 0.000001
#3.1415926 6.2830 0.00000001