# The recursive Borda method for the linear ordering problem, this is used as a subroutine in the other heuristics.
import itertools
import numpy as np
import random
from function import trans_matrix
from exact import gurobi_solve

def calc_beta(X,B,beta):
    for i in X:
        for j in X:
            if i != j:
                w = B[i][j] - B[j][i]
                if w != 0:
                    beta[i] += w
                    beta[j] += -w
    return beta

def calc_gamma2(D,beta):
    row = np.sum(D,axis=0)
    col = np.sum(D,axis=1)
    for i in range(len(D)):
        beta[i] = row[i] - col[i]
    return beta

def max2op(X_k,beta):
    TB = [[],[]]
    for i in X_k:
        if beta[i] > 0:
            TB[0].append(i)
        else:
            TB[1].append(i)
    return TB

# Max2op with random tie-breaking
def random_max2op(X_k,beta,alpha):
    TB = [[],[]]
    max_b = max(beta)
    min_b = min(beta)
    for i in X_k:
        if beta[i] > max_b*alpha:
            TB[0].append(i)
        elif beta[i] < min_b*alpha:
            TB[1].append(i)
        else:
            if random.random() >= 0.5:
                TB[0].append(i)
            else:
                TB[1].append(i)
    return TB

def rBorda(B, MAXSIZE):
    n = B.shape[0]
    B_copy = B.copy()
    D = trans_matrix(B_copy)

    X = [[i for i in range(n)]]
    gamma = [0 for i in range(n)]

    length = len(X)
    i = 0
    while i < length:
        if len(X[i]) > MAXSIZE:
            beta = [0 for i in range(n)]
            beta = calc_beta(X[i],D,beta)
            if max(beta) == min(beta):
                i = i + 1
                continue
            X[i:i+1] = max2op(X[i],beta)
            length = length + 1
            #print(X)
        else:
            i = i + 1

    B_copy = B.copy()
    sigma = []
    #カットに応じた行列の抽出&Gurobi
    for k in range(len(X)):
        if len(X[k]) == 1:
            sigma.append(list(X[k]))
        else:
            B_k = B_copy[np.ix_(X[k],X[k])]
            sigma_normal = gurobi_solve(B_k,len(X[k]))
            #exit()
            sigma_k = np.array(X[k])
            sigma_k = sigma_k[sigma_normal]
            sigma.append(sigma_k)
    #print(sigma)
    sigma = list(itertools.chain.from_iterable(sigma))
    return sigma