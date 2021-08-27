import os
import numpy as np
import pandas as pd
from sklearn.cluster import DBSCAN
import plotly.express as px
import plotly.graph_objects as go
from DataLoader import Meta
from DataLoader import ChampLoc
from distances.compute_distance_matrix import compute_distance_matrix
from PIL import Image
from collections import Counter


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
    df = pd.concat([df, pd.Series(prefix, name='prefix')], axis=1, ignore_index=True)
    df.columns = ['x', 'y', 'label', 'name']
    return df


def add_timestamp(df):
    timestamp = []
    for name, count in df.name.value_counts(sort=False).items():
        for t in range(count):
            timestamp.append(t)
    df['timestamp'] = timestamp
    return df


def visualization(df):
    map = Image.open("./data/map.png")
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


def visualization_label(df, label):
    map = Image.open("./data/map.png")
    df.label = df.label.astype('int').astype('str')
    fig = px.scatter(df[df.label == str(label)]
                     , x='x', y='y', color="timestamp", hover_data=['name'])
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


def auxiliary_data(df, auxiliary=False):
    map = Image.open("./data/map.png")

    df.columns = ['x', 'y', 'label', 'name']
    df.label = df.label.astype('int').astype('str')
    fig = px.scatter(df[df.name == 'sNW-KwhVqZs'],
                     x='x', y='y', color="label", hover_data=['name'])

    if auxiliary == True:
        fig.add_trace(
            go.Scatter(
                x=np.random.normal(0.75, 0.01, size=10),
                y=np.random.normal(0.45, 0.01, size=10),
                mode='markers',
                marker_color='rgba(152, 0, 0, .8)'
            )
        )

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
    cl = clustering(dist_mat, eps=0.2, min_samples=1)
    print(Counter(cl.labels_))
    df = prepare_visualization(trajectories, cl)
    df = add_prefix(df)
    df = add_timestamp(df)
    visualization(df)