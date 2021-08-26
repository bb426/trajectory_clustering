"""
References: https://towardsdatascience.com/gps-trajectory-clustering-with-python-9b0d35660156
"""
import numpy as np
import similaritymeasures


def compute_distance_matrix(trajectories):
    """
    :param method: "Frechet" or "Area"
    """
    n = len(trajectories)
    dist_m = np.zeros((n, n))
    for i in range(n - 1):
        p = trajectories[i]
        for j in range(i + 1, n):
            q = trajectories[j]
            dist_m[i, j] = similaritymeasures.frechet_dist(p, q)
            dist_m[j, i] = dist_m[i, j]
    return dist_m