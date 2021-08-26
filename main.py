import os
import numpy as np
import pandas as pd
from sklearn.cluster import DBSCAN
import plotly.express as px
from DataLoader import Meta
from DataLoader import ChampLoc
from distances.compute_distance_matrix import compute_distance_matrix
from PIL import Image




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
    dist_mat = compute_distance_matrix(trajectories)
    return trajectories, dist_mat


def clustering(dist_mat, eps, min_samples):
    cl = DBSCAN(eps=eps, min_samples=min_samples, metric='precomputed')
    cl.fit(dist_mat)
    return cl


def prepare_visualization(trajectories, cl):
    labels = cl.labels_
    for i, (t, label) in enumerate(zip(trajectories, labels)):
        n = len(t)
        label_added = np.c_[t, np.ones(n) * label]
        if i == 0:
            data = label_added
        else:
            data = np.r_[data, label_added]
    return pd.DataFrame(data, columns=['x', 'y', 'label'])


def add_prefix(df):
    fp = './data/opgg_data_project'
    prefix = []
    for name, t in zip(os.listdir(fp), trajectories):
        for n in range(len(t)):
            prefix.append(name)
    return pd.concat([df, pd.Series(prefix, name='prefix')], axis=1, ignore_index=True)


def visualization(df):
    map = Image.open("./data/map.png")

    df.columns = ['x', 'y', 'label', 'name']
    df.label = df.label.astype('int').astype('str')
    fig = px.scatter(df, x='x', y='y', color="label", hover_data=['name'])
    fig.add_layout_image(
        dict(
            source=map,
            xref="x",
            yref="y",
            x=0,
            y=1,
            sizex=1,
            sizey=1,
            sizing="stretch",
            opacity=0.5,
            layer="below"
            )
                        )
    fig.show()


if __name__ == '__main__':
    trajectories, dist_mat = preprocessing()
    cl = clustering(dist_mat, eps=0.3, min_samples=1)
    df = prepare_visualization(trajectories, cl)
    df = add_prefix(df)
    visualization(df)