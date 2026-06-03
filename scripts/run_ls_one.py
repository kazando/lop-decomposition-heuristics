# A wrapper for constructive heuristic method for the linear ordering problem
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT / "src"))
import time
import argparse

from local_search import neighbour_insert
from function import read_matrix, calc_fitness
from mincut import mincut_method
from level_graph import level
from recursive_borda import rBorda
from baselines import becker_static, becker, borda, borda_sequential

METHODS = {
    "becker": becker,
    "becker_static": becker_static,
    "borda": borda,
    "borda_sequential": borda_sequential,
    "mincut": mincut_method,
    "level": level,
    "rborda": rBorda
}

argparse = argparse.ArgumentParser(description="Local search for the linear ordering problem")
argparse.add_argument("--instance", type=str, help="Path to the instance file")
argparse.add_argument("--method", type=str, choices=METHODS.keys(), help="Constructive heuristic method for the initial solution")
argparse.add_argument("--maxsize", type=int, default=40, help="Maximum size of the subsets to solve exactly with Gurobi")  

if __name__ == '__main__':
    args = argparse.parse_args()
    instance = args.instance
    method = args.method
    MAXSIZE = args.maxsize
    print(instance)
    
    start = time.time()
    B = read_matrix(instance)
    if method in {"mincut", "level", "rborda"}:
        sigma = METHODS[method](B, MAXSIZE)
    else:
        sigma = METHODS[method](B)
    
    sigma = neighbour_insert(B, sigma)
    end = time.time()
    obj = calc_fitness(B, sigma)
    print(f"time [s]: {end - start}")
    print(f"objective value: {obj}")