from math import sin, sqrt

from numpy import double, sign


def func(x):
    return double(sin(x) * x ** 2)


def brent(a: double, c: double, eps: double):
    k = (3 - sqrt(5)) / 2
    x = w = v = (a + c) / 2
    fx = fw = fv = func(x)
    d = e = c - a
    iter_counter = 0
    func_counter = 1
    lengths = []
    while True:
        iter_counter += 1
        lengths.append(c - a)
        g = e
        e = d
        flg = True
        if (x != w) & (x != v) & (w != v) & (fx != fw) & (fx != fv) & (fw != fv):
            u = x - (((x - w) ** 2) * (fx - fv) - ((x - v) ** 2) * (fx - fw)) / (
                    2 * (x - w) * (fx - fv) - (x - v) * (fx - fw))
            if a + eps <= u <= c - eps and abs(u - x) < g / 2:
                d = abs(u - x)
                flg = False
        if flg:
            if x < (c + a) / 2:
                u = x + k * (c - x)
                d = c - x
            else:
                u = x - k * (x - a)
                d = x - a
        fu = func(u)
        func_counter += 1
        if (c - a) < eps:
            return (u + x) / 2, iter_counter, func_counter, lengths
        if fu <= fx:
            if u >= x:
                a = x
            else:
                c = x
            v = w
            w = x
            x = u
            fv = fw
            fw = fx
            fx = fu
        else:
            if u >= x:
                c = u
            else:
                a = u
            if fu <= fw and w == x:
                v = w
                w = u
                fv = fw
                fw = fu
            elif fu <= fv and v == x and v == w:
                v = u
                fv = fu


a, b, e = map(double, input().split())
print("======brent======")
print("Eps = ", e)
minimum, iter_counter, func_counter, lengths = (brent(a, b, e))
print("Minimum point is " + str(minimum) + "\nIteration number : " + str(iter_counter) + "\nFunction calculation "
                                                                                         "number : " + str(
    func_counter))
print("Values step by step :")
print(lengths)


print()
for i in range(1, len(lengths)):
    print(lengths[i]/lengths[i-1])