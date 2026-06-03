import gurobipy as gp
import itertools
#######################################################################################################################
# Gurobi solver for the linear ordering problem. 
# This function is used to solve the subproblems in the constructive heuristic methods. It takes a matrix B and 
# the size of the subproblem m as input and returns the optimal permutation sigma2.
#######################################################################################################################
env = gp.Env()
env.setParam('OutputFlag', 0)

def gurobi_solve(B,m):
    # Declaration of the Gurobi model
    model = gp.Model(name='GurobiSolve', env=env)

    # Declaration of decision variables
    x = {}
    for i in range(m):
        for j in range(m):
            x[i, j] = model.addVar(vtype=gp.GRB.BINARY)

    # objective function
    model.setObjective(gp.quicksum(B[i, j] * x[i, j] for j in range(m) for i in range(m)), sense=gp.GRB.MINIMIZE)

    # constraints
    for i in range(m):
        for j in range(i+1, m):
            model.addConstr(x[i, j] + x[j, i] == 1)
    n = [i for i in range(m)]
    for c in itertools.combinations(n,3):
        model.addConstr(x[c[0], c[1]]+x[c[1], c[2]]+x[c[2], c[0]] >= 1)
        model.addConstr(x[c[2], c[1]]+x[c[1], c[0]]+x[c[0], c[2]] >= 1)

    #print("##### Gurobi Log #####")
    model.optimize()
    #print()
    
    sigma1 = [0 for i in range(m)]
    sigma2 = [0 for i in range(m)]
    for i in range(m):
        for j in range(m):
            if i != j and x[i, j].X ==1:
                sigma1[i] = sigma1[i] + 1
    #print(sigma1)

    for i in range(m):
        sigma2[sigma1[i]] = i
    #print(sigma2)

    # Output the optimal solution
    #print("##### solution #####")
    # if model.Status == gp.GRB.OPTIMAL:
    #     val_opt = model.ObjVal
    #     print("Optimal Value : ", val_opt)
    # else:
    #     print("&&&&&")

    return sigma2
