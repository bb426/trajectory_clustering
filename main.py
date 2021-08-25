import os
from DataLoader import Meta
from DataLoader import ChampLoc


def preprocessing():
    meta = Meta.read_meta()
    fp = './data/opgg_data_project'
    match_names = os.listdir(fp)

    for name in match_names:
        loc = ChampLoc.LocationData(fp, meta, name)
        loc.time_condition()
        loc.crop_start
        loc.merge_files()
        loc.select_champID()
