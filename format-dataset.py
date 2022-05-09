import pandas as pd
import matplotlib.pyplot as plt
from os import listdir,  walk
from os.path import isfile, join
import haversine as hs
from haversine import Unit

# Initial variables
columns_label = ['Latitude', 'Longitude',
                 'time', 'x_projection', 'y_projection']
columns_excluded = ['Latitude', 'Longitude',
                    'time', 'x_projection', 'y_projection']
delimiter = '|'

foldername = 'dataset/custom'
colors = ['red', 'blue', 'green', 'orange', 'pink', 'black',
          'yellow', 'brown', 'corel', 'violet', 'indigo', 'teal']


file1 = '../dataset/person1/0530/gpsdata01.txt'
file2 = "../dataset/person1/0613/gpsdata-6-13-02.txt"


def listing_files(foldername):
    data_files = []
    for root, directories, files in walk(foldername, topdown=False):
        for name in files:
            filename = join(root, name)
            data_files.append(filename)
    return data_files


def read_files(list_files):
    list_dfs = []
    for filename in list_files:
        df = pd.read_csv(filename, delimiter=delimiter)
        # add columns label
        df.columns = columns_label
        list_dfs.append(df)
    return list_dfs


def preprocessing(df):
    # 1. fix (Lat, Long) issue than tuple them in new columns
    df['Longitude'] = df.Longitude / (-100)
    df['Latitude'] = df.Latitude / 100

    # sorted dataframe by 'Longitude', 'Latitude'
    df.sort_values(by=['Longitude', 'Latitude'])

    # combine (Lat, Long) in new column called coordinate
    df['coordinate'] = list(zip(df.Latitude, df.Longitude))

    # exclude unecessary columns
    df = df.loc[:, ~df.columns.isin(columns_excluded)]

    return df


def plot(dfs, colors):
    for df, color in zip(dfs, colors):
        df.plot(x="Longitude", y="Latitude", c=color)
    plt.show()


def distance_from(loc1, loc2):
    # To calculate distance in meters
    dist = hs.haversine(loc1, loc2, unit=Unit.METERS)
    return round(dist, 2)


def get_all_distance(dfs, df):
    dist_df = df.rename(columns={'coordinate': 'user'})
    #dist_df.rename(columns={'coordinate': 'user'}, inplace=True)
    # print(dist_df.columns.values)

    for i in range(1, len(dfs)):
        ms_positions = []
        print('ms length', len(dfs[i].coordinate))
        _MAX_LENGTH = len(df.coordinate)
        print(_MAX_LENGTH)
        # return
        for loc1, loc2 in zip(df.coordinate, dfs[i].coordinate):
            # print(loc1, ' ', loc2)
            distance = distance_from(loc1, loc2)
            ms_dict = {'distance': distance, 'position': loc2}
            ms_positions.append(ms_dict)

        columns_nb = len(dist_df.columns)
        dist_df.insert(columns_nb, f'ms-{columns_nb}', pd.Series(ms_positions))

    return dist_df
  
  
# Algorithm
list_files = listing_files(foldername)
print(len(list_files))

selected_files = list_files[:10]
dfs = read_files(selected_files)
# print(dfs[0].head())

for index, df in enumerate(dfs):
    dfs[index] = preprocessing(df)
# print(dfs[0].head())

#plot(dfs, colors)

user_df = dfs[0]

df = get_all_distance(dfs, user_df)

print(df.iloc[500])
