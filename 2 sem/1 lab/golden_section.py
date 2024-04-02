from math import sin, sqrt

from numpy import double


def func(x):
    return double(sin(x) * x ** 2)


def golden_section(a, b, e):
    x1 = a + ((-sqrt(5) + 3) / 2) * (b - a)
    x2 = a + ((sqrt(5) - 1) / 2) * (b - a)
    f1 = func(x1)
    f2 = func(x2)
    iter_counter = 0
    func_counter = 2
    lengths = [b - a]
    print(x1, x2)
    while (b - a > e):
        if f1 > f2:
            a = x1
            x1 = x2
            x2 = a + ((sqrt(5) - 1) / 2) * (b - a)
            f1 = f2
            f2 = func(x2)
        else:
            b = x2
            x2 = x1
            x1 = a + ((-sqrt(5) + 3) / 2) * (b - a)
            f2 = f1
            f1 = func(x1)
        iter_counter += 1
        func_counter += 1
        lengths.append(b - a)
    return (a + b) / 2, iter_counter, func_counter, lengths


a, b, e = map(double, input().split())
print("======golden_section======")
print("Eps = ", e)
minimum, iter_counter, func_counter, lengths = (golden_section(a, b, e))
print("Minimum point is " + str(minimum) + "\nIteration number : " + str(iter_counter) + "\nFunction calculation "
                                                                                         "number : " + str(
    func_counter))
print("Values step by step :")
print(lengths)

for i in range (1, len(lengths)):
    print(lengths[i]/lengths[i-1], "  ", i)

# -3.1415926 0 0.000001    -2.2889296501919363
# (-2.2889296524283074, 3  -2.288929652664881
# 3                        -2.2889296501919363
# 4,

#(5.086985090868577, 40, 41, [3.1414074000000003, 2.1706591271447815, 1.5707037000000001, 0.9707482728552179, 0.5999554271447813, 0.23899188443673403, 0.09736162016064309, 0.04326367304280687, 0.022600095965387368, 0.012770792962998101, 0.009969592564138985, 0.005091583715562287, 0.003228350132828517, 0.0020768084497184702, 0.0012835382100488957, 0.0012346106791456535, 0.0006300142515431872, 0.0003990789656755922, 0.00025635310980742787, 0.00015843493498302053, 0.00014892848784597845, 6.692343459135941e-05, 3.560029149785038e-05, 2.363591547016597e-05, 1.6241524431137577e-05, 1.0037814127450417e-05, 9.652940216042794e-06, 4.361910590056084e-06, 2.3409171081567592e-06, 1.568966289333673e-06, 1.0918744450805207e-06, 6.748155181313109e-07, 6.334911919481101e-07, 2.9386261424235727e-07, 1.641360416471116e-07, 8.396061002002853e-08, 5.189051055509708e-08, 2.3144538729980013e-08, 1.2164554696880714e-08, 6.7860037589184685e-09])