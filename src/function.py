# Functions used in heuristics for the linear ordering problem
import numpy as np
import random
import itertools
import time

# Read the matrix from the given file. The first line of the file contains the size of the matrix, and the rest of the lines contain the matrix values.
def read_matrix(file):
    size = int(open(file, "r").readlines()[0])
    #matrix = np.loadtxt(file, delimiter=',', dtype='int64', skiprows=1)
    matrix = np.loadtxt(file, delimiter=None, dtype='int64', skiprows=1)
    return matrix

# Transform the matrix B into a form where B[i][j] represents the contribution of placing element i before element j in the solution. This is done by taking the difference between B[i][j] and B[j][i] for each pair of elements (i, j).
def trans_matrix(B):
    n = B.shape[0]
    d = 0
    for i in range(n):
        for j in range(i+1,n):
            if i != j:
                d = B[i][j] - B[j][i]
                #print(d)
            if d > 0:
                B[i][j] = d
                B[j][i] = 0
            elif d < 0:
                B[i][j] = 0
                B[j][i] = -d
            else:
                B[i][j] = 0
                B[j][i] = 0
    return B

# Calculate the objective function value for the linear ordering problem with matrix B and solution sigma.
def calc_fitness(B,sigma):
    n = B.shape[0]
    fitness = 0
    B = B[:, sigma]
    B = B[sigma, :]
    np.set_printoptions(threshold=n**2)
    #print(B)
    for i in range(n):
        for j in range(i+1, n):
            fitness = fitness + B[i][j]
    return fitness

# Perturb the matrix B by multiplying each non-zero element by a random number between s and t. This is used in the iterated local search heuristic.
def perturbation(B,s,t):
    n = B.shape[0]
    for i in range(n):
        for j in range(n):
            if B[i][j] != 0:
                epsilon = random.uniform(s, t)
                #epsilon = random.uniform(0.5, 1.5)
                B[i][j] = round(B[i][j] * epsilon)
                #print(B[i][j])
    return B


