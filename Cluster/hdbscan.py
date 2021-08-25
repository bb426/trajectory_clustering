import os
import pandas as pd
import hdbscan
from distances.frechet import FastDiscreteFrechetMatrix

parquet_files = [f for f in os.listdir('./data/filtered') if f.endswith('.parquet')]
pd.read_parquet('./data/filtered/' + parquet_files[0])

# trajectory의 각 point별 distance matrix부터 구해야함(symmetirc함)

def calculate_distance_matrix(trajectories):
    n_traj = len(trajectories)
    dist_mat = np.zeros((n_traj, n_traj), dtype=np.float64)
    dfd = FastDiscreteFrechetMatrix(earth_haversine)

    for i in range(n_traj - 1):
        p = trajectories[i]
        for j in range(i + 1, n_traj):
            q = trajectories[j]

            # Make sure the distance matrix is symmetric
            dist_mat[i, j] = dfd.distance(p, q)
            dist_mat[j, i] = dist_mat[i, j]
    return dist_mat


# if __name__ == '__main__':

dist_mat = calculate_distance_matrix(trajectories)
clusterer = hdbscan.HDBSCAN(metric='precomputed', min_cluster_size=2, min_samples=1, cluster_selection_methos='leaf')
clusterer.fit(dist_mat)
clusterer.labels_
# 이후 visualization