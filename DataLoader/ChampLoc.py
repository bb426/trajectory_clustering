class LocationData():
    def __init__(self, fp, meta, Name):
        self.fp = fp
        self.meta = meta
        self.Name = Name

    def time_condition(self, start_seconds=90, end_seconds=210):
        """
        개별 게임별(name) 1:30, 3:30초에 해당하는 file_name을 return
        :param name:
        :param start_seconds: 90초
        :param end_seconds: 210초
        :return int: crop_starting, crop_ending
        """
        record_start = self.meta.loc[self.meta['Name'] == self.Name]['StartTime']
        crop_start = record_start.map(lambda x: start_seconds - (int(x.split(':')[0]) * 60 + int(x.split(':')[1])) + 1)
        crop_end = record_start.map(lambda x: end_seconds - (int(x.split(':')[0]) * 60 + int(x.split(':')[1])) + 1)
        self.crop_start = crop_start.values[0]
        self.crop_end = crop_end.values[0]

    def merge_files(self):
        """
        각 게임(Name)별 1:30 ~ 3:30초에 해당하는 cropped txt files를 Merging
        """
        crop_files = []
        for i in range(self.crop_start, self.crop_end + 1):
            crop_files.append(f'{self.Name}_crop_{i}.txt')

        with open(f'./data/filtered/{self.Name}.txt', 'w') as outfile:
            for f in crop_files:
                with open(f'{self.fp}/{self.Name}/labels/{f}') as infile:
                    outfile.write(infile.read())

    def get_trajectory(self, ChampID=67):
        """
        특정 Champion의 위치데이터만 Slicing하여 DataFrame으로 dump
        :param ChampID: ChampID (LeeSin==67)
        :return: None
        """
        import pandas as pd

        data = pd.read_table(f'./data/filtered/{self.Name}.txt',
                             sep=' ',
                             names=['ChampID', 'x', 'y', 'width', 'height', 'confidence'])
        cond = data['ChampID'] == ChampID
        # data.loc[cond].to_parquet(f'./data/filtered/{self.Name}_{ChampID}.parquet', index=False)
        return data.loc[cond, ['x', 'y']].values

#
# import pandas as pd
# import os
# import similaritymeasures
# import numpy as np
#
# parquet_files = [f for f in os.listdir('./data/filtered') if f.endswith('.parquet')]
# tr_0 = pd.read_parquet('./data/filtered/' + parquet_files[0])[['x', 'y']].values
# tr_1 = pd.read_parquet('./data/filtered/' + parquet_files[1])[['x', 'y']].values
# tr_0.shape
# tr_1.shape
#
# df = similaritymeasures.frechet_dist(tr_0, tr_1)
# df
#
# np.zeros((3, 5, 5))
#
# data = pd.read_table(f'./data/filtered/ZhoROlQluXw.txt',
#                      sep=' ',
#                      names=['ChampID', 'x', 'y', 'width', 'height', 'confidence'])
# cond = data['ChampID'] == 67
# # data.loc[cond].to_parquet(f'./data/filtered/{self.Name}_{ChampID}.parquet', index=False)
# data.loc[cond, ['x', 'y']].values