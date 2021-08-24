import yaml
import pandas as pd

with open('./data/champion_class_id.yaml') as f:
    ChampClass = yaml.load(f, Loader=yaml.FullLoader)
    print(pd.DataFrame(ChampClass))


