# The level graph method for the linear ordering problem. This is used as a subroutine in the other heuristics.
import networkx as nx
import numpy as np
from function import trans_matrix
import itertools
from exact import gurobi_solve

# Sort the entries of the input matrix in ascending order
def sort_entries(B):
    sorted_entries = itertools.chain.from_iterable(B)
    return sorted(set(sorted_entries))

# Sort the absolute differences of the entries of the input matrix in ascending order
def sort_diff(B):
    n = B.shape[0]
    Lambda = []
    for i in range(n):
        for j in range(i,n):
            Lambda.append(abs(B[i][j]-B[j][i]))
    return sorted(set(Lambda))

# Generate a directed graph from the input matrix and a threshold value
def trans_matrix_lambda(X,B,Lambda_j):
    G = nx.DiGraph()
    for i in X:
        G.add_node(i)
        for j in X:
            if i != j:
                if B[i][j] > Lambda_j:
                    G.add_edge(i,j)
    return G

# Partition the input set into strongly connected components based on the input matrix and a threshold value
def topological_sort(X_j,G_j,number):
    X_ts = list(X_j)
    G_ts = nx.DiGraph()
    for k in range(len(X_ts)):
        #X_ts[k] = list(X_ts[k])
        for n in X_ts[k]:
            number[n] = k
    #print(number)
    for k in range(len(X_ts)):
        G_ts.add_node(k)
        for (i,j) in G_j.edges():
            if number[i] != number[j]:
                G_ts.add_edge(number[i],number[j])
    t_s = list(nx.topological_sort(G_ts))
    return t_s

def partition(Lambda,Y,B,number):
    W = list(Y[1])
    G_j = trans_matrix_lambda(W,B,Lambda[Y[0]+1])
    X_j = list(nx.strongly_connected_components(G_j))
    k = len(X_j)
    if k > 1:
        t_s = topological_sort(X_j,G_j,number)
    else:
        t_s = [0]
    Z = [[] for l in range(k)]
    for l in range(k):
        Z[l].append(Y[0]+1)
        Z[l].append(X_j[t_s[l]])
    return k,Z
#
def level(B, MAXSIZE):
    D = trans_matrix(B)
    n = B.shape[0]

    Lambda = sort_diff(B)

    X = [[-1, {i for i in range(n)}]]
    number = [0 for i in range(n)]

    length = len(X)
    i = 0

    while i < length:
        if len(X[i][1]) > MAXSIZE:
            k,X[i:i+1] = partition(Lambda,X[i],D,number)
            length = length + (k-1)
        else:
            i = i + 1
    #print(X)

    B_copy = B.copy()
    sigma = []

    #
    for k in range(len(X)):
        if len(X[k][1]) == 1:
            sigma.append(list(X[k][1]))
        else:
            B_k = B_copy[np.ix_(list(X[k][1]),list(X[k][1]))]
            sigma_normal = gurobi_solve(B_k,len(X[k][1]))
            sigma_k = np.array(list(X[k][1]))
            #exit()
            #print(sigma_k)
            sigma_k = sigma_k[sigma_normal]
            sigma.append(sigma_k)
    sigma = list(itertools.chain.from_iterable(sigma))

    return sigma
