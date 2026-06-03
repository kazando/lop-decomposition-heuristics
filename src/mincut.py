# The minimum cut method for the linear ordering problem, using Hao-Orlin's algorithm for minimum cut. This is used as a subroutine in the other heuristics.
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT / "cpp"))
import hao_orlin_cpp
import networkx as nx
import numpy as np
import itertools
import math
from function import trans_matrix
from exact import gurobi_solve
# 
def make_graph(D,Y):
    G = nx.DiGraph()
    for i in Y:
        G.add_node(i)
        for j in Y:
            if D[i][j] > 0:
                G.add_edge(i,j,capacity=D[i][j])
    return G

# obsolete, use minimum_cut_HO instead
def minimum_cut(D,Y):
    Y = list(Y)
    i = Y[0]
    min_w = math.inf
    G = make_graph(D,Y)
    for j in Y:
        if i != j:
            cut_value,partition = nx.minimum_cut(G,i,j)
            if cut_value < min_w:
                min_w = cut_value
                min_p = list(partition)
            cut_value,partition = nx.minimum_cut(G,j,i)
            if cut_value < min_w:
                min_w = cut_value
                min_p = list(partition)
    min_p.reverse()
    print("------")
    print(min_p)
    return min_p

# Minimum cut method for the linear ordering problem, using Hao-Orlin's algorithm for minimum cut
def minimum_cut_HO(D,Y):
    G = make_graph(D,Y)
    node_list = list(G.nodes())
    index = {node: i for i, node in enumerate(node_list)}

    edges = []
    for u, v, data in G.edges(data=True):
        edges.append((index[u], index[v], float(data["capacity"])))

    res = hao_orlin_cpp.min_cut_with_partition(len(node_list), edges)

    S = {node_list[i] for i in res["S"]}
    T = {node_list[i] for i in res["T"]}

    #return {
    #    "value": res["value"],
    #    "S": S,
    #    "T": T
    #}
    return [T,S]

def mincut_method(B,MAXSIZE):
    D = trans_matrix(B)
    n = B.shape[0]

    X = [{i for i in range(n)}]
    length = len(X)
    i = 0

    while i < length:
        if len(X[i]) > MAXSIZE:
            X[i:i+1] = minimum_cut_HO(D,X[i])
            #print(X)
            length = length + 1
        else:
            i = i + 1
    #print(X)
    # exit()

    B_copy = B.copy()
    sigma = []
    #最小カットに応じた行列の抽出&Gurobi
    for k in range(len(X)):
        if len(X[k]) == 1:
            sigma.append(list(X[k]))
        else:
            B_k = B_copy[np.ix_(list(X[k]),list(X[k]))]
            sigma_normal = gurobi_solve(B_k,len(X[k]))
            sigma_k = np.array(list(X[k]))
            sigma_k = sigma_k[sigma_normal]
            sigma.append(sigma_k)
    #print(sigma)
    sigma = list(itertools.chain.from_iterable(sigma))
    #print('##########')
    #print(sigma)
    #exit()


    #print(end_time)
    #print(fitness)

    return sigma