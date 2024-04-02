import math
import time
from random import randint

import numpy
from numpy import array, pi
from numpy.random import random
from scipy.sparse import csr_matrix


start_time = time.time()


def create_csr_matrix():
    arr = array([0. for i in range(n*n)]).reshape(n, n)
    for i in range(n):
        for j in range(i, n):
            if i != j:
                arr[i][j] = randint(0, 5)
                arr[j][i] = arr[i][j]
    for i in range(n):
        arr[i][i] = sum(arr[i][j] for j in range(n)) + 10**(-k)
    return csr_matrix(arr,  dtype=float)


def Gilbert_matrix_generator():
    arr = array([0. for i in range(n * n)]).reshape(n, n)
    for i in range(n):
        for j in range(i, n):
            arr[i][j] = 1/(i+j+1)
            arr[j][i] = arr[i][j]
    return csr_matrix(arr, dtype=float)


def jakobi():
    it = 0 # Количетсво итераций
    dataUN, indicesUN, indptrUN = [], [], [0] * (n + 1)
    for k in range(n):
        indptrUN[k + 1] = k + 1
        dataUN.append(1)
        indicesUN.append(k)
    UN = csr_matrix((dataUN, indicesUN, indptrUN), dtype=float) # Создаем массив в котором будет хранится значения собственных векторов
    A = a.copy() #
    maxnumber = 2 * eps
    while abs(maxnumber) > eps:
        it += 1
        maxnumber = 0
        i, j = 0, 0
        aii, ajj = 0, 0
        # Ищем максимальный элемент и его координаты в матрице
        for k in range(len(A.data)):
            stringnumber = 1
            while A.indptr[stringnumber] <= k:
                stringnumber += 1
            stringnumber -= 1
            if abs(A.data[k]) >= abs(maxnumber) and A.indices[k] != stringnumber:
                maxnumber = A.data[k]
                i = stringnumber
                j = A.indices[k]
        if i > j:
            k = i
            i = j
            j = k
        # Ищем диагональные элементы
        for k in range(A.indptr[i], A.indptr[i + 1]):
            if A.indices[k] == i:
                aii = A.data[k]
        for k in range(A.indptr[j], A.indptr[j + 1]):
            if A.indices[k] == j:
                ajj = A.data[k]
        # Ищем угол фи и его косинус/синус
        if aii - ajj == 0:
            fi = pi/4
        else:
            fi = numpy.arctan(2 * maxnumber / (aii - ajj)) / 2
        cosfi = numpy.cos(fi)
        sinfi = numpy.sin(fi)
        # Создаем матрицу поворота и ее транспортируемую копию
        dataU, indicesU, indptrU = [], [], [0]*(n+1)
        for k in range(n):
            indptrU[k+1] = k+1
        for g in range(i, n):
            indptrU[g + 1] += 1
        for g in range(j, n):
            indptrU[g + 1] += 1
        for k in range(n):
            if k == i:
                dataU.append(cosfi)
                indicesU.append(i)
                dataU.append(-sinfi)
                indicesU.append(j)
            elif k == j:
                dataU.append(sinfi)
                indicesU.append(i)
                dataU.append(cosfi)
                indicesU.append(j)
            else:
                dataU.append(1)
                indicesU.append(k)
        U = csr_matrix((dataU, indicesU, indptrU), dtype=float)
        Utransp = U.transpose()
        # считаем матрицу A
        A = (Utransp.dot(A)).dot(U)
        UN = UN.dot(U)

        # print(maxnumber)
        # print(U.toarray())
    print("Матрица собственных значений\n", A.toarray())
    print("Матрица столбцы которой являются собственными векторами\n", UN.toarray())
    print(it)


n = 25
eps = 0.001
k = 7
q1 = [[2.2, 1, 0.5, 2], [1, 1.3, 2, 1], [0.5, 2, 0.5, 1.6], [2, 1, 1.6, 2]]
q2 = [[5, 1, 2], [1, 4, 1], [2, 1, 3]]
# a = Gilbert_matrix_generator()
# a = csr_matrix(q1, dtype=float
a = create_csr_matrix()
print("Изначальная матрица \n", a.toarray())
# print(create_csr_matrix().toarray())
print(jakobi())
print(n)
print("--- %s seconds ---" % (time.time() - start_time))
# a = Gilbert_matrix_generator()
# print (a.toarray())
