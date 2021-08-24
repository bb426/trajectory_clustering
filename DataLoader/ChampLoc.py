# opgg_data_project/밑의 데이터를 각각 읽고
# leesin 로그만 딴다음에
# 1:30초 이후 로그만 선택

import os

import pandas as pd

from DataLoader import Meta
names = os.listdir('./data/opgg_data_project/')
meta = Meta.read_meta()



class LocationData(self, fp, meta, Name, ChampID=67):
    def __init__(self):
        self.fp = fp
        self.meta = meta
        self.Name = Name
        self.ChampID = ChampID
        # self.names = os.listdir(fp)

    def time_condition(self, start_seconds=90, end_seconds=210):
        """
        개별 게임별(name) 1:30, 3:30초에 해당하는 file_name을 return
        :param name:
        :param start_seconds: 90초
        :param end_seconds: 210초
        :return int: crop_starting, crop_ending
        """
        crops = os.listdir(f'{self.fp}/{self.Name}/labels/')
        record_start = self.meta[self.meta.loc['Name'] == self.Name]['StartTime']
        crop_start = record_start.map(lambda x: start_seconds - (int(x.split(':')[0]) * 60 + int(x.split(':')[1])) + 1)
        crop_end = record_start.map(lambda x: end_seconds - (int(x.split(':')[0]) * 60 + int(x.split(':')[1])) + 1)
        self.crop_start = crop_start
        self.crop_end = crop_end

    def get_data(self):
        # filenames = ['file1.txt', 'file2.txt', ...]
        # with open('path/to/output/file', 'w') as outfile:
        #     for fname in filenames:
        #         with open(fname) as infile:
        #             outfile.write(infile.read())



27
147
fp = './data/opgg_data_project/'
folder = 'ZhoROlQluXw'
os.listdir(f'{fp}/{folder}/labels/')

temp = []
for i in range(27, 147 + 1):
    temp.append(f'{folder}_crop_{i}.txt')

temp

with open(f'./data/opgg_data_project/filtered/{folder}.txt', 'w') as outfile:
    for f in temp:
        with open(f'./data/opgg_data_project/{folder}/labels/{f}') as infile:
            outfile.write(infile.read())

filenames = ['file1.txt', 'file2.txt', ...]
with open('path/to/output/file', 'w') as outfile:
    for fname in filenames:
        with open(fname) as infile:
            outfile.write(infile.read())

temp3 = pd.read_table(f'./data/opgg_data_project/filtered/{folder}.txt', sep=' ',
                      names=['ChampID', 'x', 'y', 'width', 'height', 'confidence'])
temp3.shape
120 * 10
temp3.head()

len(temp)