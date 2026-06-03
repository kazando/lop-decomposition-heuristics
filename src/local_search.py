import numpy as np
import time
#######################################################################################################################
# Local search with insertion neighborhood for the linear ordering problem, with a time limit of 1 hour. This is used in the iterated local search heuristic.
#######################################################################################################################
def best_permutation(B,sigma_normal):
    n = len(sigma_normal)
    if n <= 1:
        return 0, sigma_normal

    max_diff = 0
    tmp_i = None
    tmp_j = None

    for i in range(n):
        x = sigma_normal[i]
        # D_i[z] = B[x][sigma[z]] - B[sigma[z]][x]
        # 挿入差分を累積和で高速に計算する
        D_i = B[x, sigma_normal] - B[sigma_normal, x]
        prefix = np.concatenate(([0], np.cumsum(D_i, dtype=np.float64)))

        if i > 0:
            diff_left = prefix[i] - prefix[:i]
            j_left = int(np.argmax(diff_left))
            if diff_left[j_left] > max_diff:
                max_diff = float(diff_left[j_left])
                tmp_i = i
                tmp_j = j_left

        if i < n - 1:
            diff_right = -(prefix[i + 2:] - prefix[i + 1])
            if diff_right.size > 0:
                j_right = int(np.argmax(diff_right))
                if diff_right[j_right] > max_diff:
                    max_diff = float(diff_right[j_right])
                    tmp_i = i
                    tmp_j = i + 1 + j_right

    if max_diff != 0:
        tmp_normal = sigma_normal[tmp_i]
        sigma_normal = np.delete(sigma_normal, tmp_i)
        sigma_normal = np.insert(sigma_normal, tmp_j, tmp_normal)

    return max_diff, sigma_normal

# local search with insertion neighborhood, with a time limit of 1 hour
def neighbour_insert(B,sigma_normal):
    max_diff = -1
    count = 0
    start = time.time()
    while max_diff != 0:
        max_diff,sigma_normal = best_permutation(B,sigma_normal)
        #count += 1
        if time.time() - start > 3600:             # time limit (3600 seconds = 1 hour)
            break
    #print(count)
    return sigma_normal