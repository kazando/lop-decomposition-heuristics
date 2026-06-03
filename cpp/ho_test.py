import sys
sys.path.append("../build")
import hao_orlin_cpp

n = 4
edges = [
    (0,1,3.0),
    (1,0,3.0),
    (1,2,2.0),
    (2,1,2.0),
    (2,3,4.0),
    (3,2,4.0),
    (0,3,1.0),
    (3,0,1.0)
]



# ----------- only min cut valur -----------
value = hao_orlin_cpp.min_cut(n, edges)
print("min cut value:", value)

# ----------- min cut with partition  -----------
res = hao_orlin_cpp.min_cut_with_partition(n, edges)

print("value:", res["value"])
print("S:", res["S"])
print("T:", res["T"])

