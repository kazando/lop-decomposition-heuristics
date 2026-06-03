# Becker's heuristic for the linear ordering problem and Borda method for the linear ordering problem
import numpy as np
import itertools
import math

# (Static) Borda
def borda(D):
    sigma = []
    gamma={}
    col = np.sum(D,axis=0) #column sum
    row = np.sum(D,axis=1) #row sum
    for i in range(len(D)):
       gamma[i] = row[i]-col[i]
    sigma = list(dict(sorted(gamma.items(), key=lambda x:x[1], reverse=True)).keys())
    
    return sigma

# Sequential Borda
def borda_sequential(D):
    sigma = []
    n = len(D)
    active = np.ones(n, dtype=bool)
    row = np.sum(D, axis=1).astype(np.int64)
    col = np.sum(D, axis=0).astype(np.int64)

    for _ in range(n):
        index = None
        max_val = None
        for i in range(n):
            if not active[i]:
                continue
            val = row[i] - col[i]
            if index is None or val > max_val:
                index = i
                max_val = val

        if index is None:
            break

        sigma.append(index)
        active[index] = False

        row -= D[:, index]
        col -= D[index, :]
        row[index] = 0
        col[index] = 0

    return sigma

# A static variation of Becker's heuristic
def becker_static(D):
    sigma = []
    qi_0 = {}
    qi_1 = {}
    qi_2 = {}
    col = np.sum(D,axis=0) # column sum vector
    row = np.sum(D,axis=1) # row sum vector
    for i in range(len(D)):
        if col[i] == 0:
            if row[i] == 0:
                qi_0[i] = math.inf
            else:
                qi_1[i] = row[i]
        else:
            qi_2[i] = row[i] / col[i]
    qi_0 = list(qi_0.keys())
    qi_1 = list(dict(sorted(qi_1.items(), key=lambda x:x[1], reverse=True)).keys())
    qi_2 = list(dict(sorted(qi_2.items(), key=lambda x:x[1], reverse=True)).keys())
    sigma.extend(qi_0)
    sigma.extend(qi_1)
    sigma.extend(qi_2)
    
    return sigma

# (Sequential) Becker's heuristic
def becker(D):
    sigma = []
    n = len(D)
    active = np.ones(n, dtype=bool)
    row = np.sum(D, axis=1)
    col = np.sum(D, axis=0)

    for _ in range(n):
        index = None
        max_row = -1
        max_q = -1
        judge = False  # col[i] == 0 の候補がまだ決まっていない状態

        for i in range(n):
            if not active[i]:
                continue

            if col[i] == 0:
                if row[i] == 0:
                    index = i
                    break
                if row[i] > max_row:
                    max_row = row[i]
                    index = i
                    judge = True
            elif not judge:
                q_i = row[i] / col[i]
                if q_i > max_q:
                    max_q = q_i
                    index = i

        if index is None:
            break

        sigma.append(index)
        active[index] = False

        row -= D[:, index]
        col -= D[index, :]
        row[index] = 0
        col[index] = 0

    return sigma

def test_becker():
    B=np.array([[0, 2, 9, 5, 0], [6, 0, 2, 1,4], [2, 8, 0, 7, 5], [3, 1, 2, 0, 4], [0, 5, 2, 7, 0]])
    B_copy = B.copy()
    #D=trans_matrix_D(B_copy,5)
    sigma = becker(B_copy)
    print(sigma)
    fitness = calc_fitness(B,m,sigma)
    print(fitness)
    
def test_borda():
    B=np.array([[0, 2, 9, 5, 0], [6, 0, 2, 1,4], [2, 8, 0, 7, 5], [3, 1, 2, 0, 4], [0, 5, 2, 7, 0]])
    B_copy = B.copy()
    #D=trans_matrix_D(B_copy,5)
    m=B.shape[0]
    sigma = borda(B_copy)
    print(sigma)
    fitness = calc_fitness(B,m,sigma)
    print(fitness)
