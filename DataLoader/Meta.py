def read_meta():
    import pandas as pd
    data = pd.read_table('./data/meta.txt', sep=',', names=['Name', 'MatchID', 'StartTime'])
    return data