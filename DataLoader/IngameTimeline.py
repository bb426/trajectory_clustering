import json
from urllib.request import urlopen
import pandas as pd


def load_timeline(url="https://opgg-data-analytics.s3.ap-northeast-2.amazonaws.com/recruit/202108/processed/5291299018+(1).json"):
    response = urlopen(url)
    data_json = json.loads(response.read())
    return data_json


def select_jg_data(data_json, participantId='2'):
    frames = pd.json_normalize(data_json['frames']).iloc[1:5, :]
    jg_cols = [col for col in frames.columns if participantId in col]
    return frames[jg_cols]


if __name__ == '__main__':
    data_json = load_timeline()
    df_jg = select_jg_data(data_json)
    print(df_jg[['participantFrames.2.jungleMinionsKilled', 'participantFrames.2.xp']])
