import os
from DataLoader import Meta
from DataLoader import ChampLoc


def preprocessing():
    meta = Meta.read_meta()
    fp = './data/opgg_data_project'
    match_names = os.listdir(fp)

    trajectories = []
    for name in match_names:
        loc = ChampLoc.LocationData(fp, meta, name)
        loc.time_condition()
        loc.crop_start
        loc.merge_files()
        trajectory = loc.get_trajectory()
        trajectories.append(trajectory)
    return trajectories

def clustering(trajectories:list):
    from distances.compute_distance_matrix import compute_distance_matrix
    dist_mat = compute_distance_matrix(trajectories)

    trajectories = preprocessing()



dist_mat
import hdbscan
clusterer = hdbscan.HDBSCAN(metric='precomputed', min_cluster_size=2, min_samples=1, cluster_selection_methos='leaf')
clusterer.fit(dist_mat)
clusterer.labels_

"""
if __name__ == '__main__':
    trajectories = preprocessing()
"""