import pandas as pd
import matplotlib.pyplot as plt
from os import listdir,  walk
from os.path import isfile, join
import haversine as hs
from haversine import Unit
from utils import plot_trajectory

# Initial variables
columns_label = ['Latitude', 'Longitude',
                 'time', 'x_projection', 'y_projection']
columns_excluded = ['Latitude', 'Longitude',
                 'time','x_projection', 'y_projection']
delimiter = '|'

foldername = 'dataset/custom'
colors = ['red', 'blue', 'green', 'orange', 'pink', 'black',
          'yellow', 'brown', 'green', 'violet', 'indigo', 'teal']

def listing_files(foldername):
    list_files = []
    for root, directories, files in walk(foldername, topdown=False):
        for name in files:
            filename = join(root, name)
            list_files.append(filename)
    return list_files


def read_files(list_files):
    list_dataframes = []
    for filename in list_files:
        df = pd.read_csv(filename, delimiter=delimiter)
        # add columns label
        df.columns = columns_label
        df = preprocessing(df)
        list_dataframes.append(df)
    return list_dataframes


def preprocessing(df):
    # 1. fix (Lat, Long) issue than tuple them in new columns
    df['Longitude'] = df.Longitude / (-100)
    df['Latitude'] = df.Latitude / 100

    # sorted dataframe by 'Longitude', 'Latitude'
    df.sort_values(by=['Longitude', 'Latitude'])

    # combine (Lat, Long) in new column called coordinate
    df['coordinate'] = list(zip(df.Latitude, df.Longitude))

    # remove unnecessary columns
    df = df.loc[:, ~df.columns.isin(columns_excluded)]

    return df

def distance_from(loc1, loc2):
    # To calculate distance in meters
    dist = hs.haversine(loc1, loc2, unit=Unit.METERS)
    return round(dist, 2)


def get_all_distance(dfs, df):
    dist_df = df.rename(columns={'coordinate': 'user'})  

    for i in range(1, len(dfs)):
        ms_positions = []
        for loc1, loc2 in zip(df.coordinate, dfs[i].coordinate):
            distance = distance_from(loc1, loc2)
            ms_dict = {'distance': distance, 'position': loc2}
            ms_positions.append(ms_dict)

        columns_nb = len(dist_df.columns)
        dist_df.insert(columns_nb, f'ms-{columns_nb}', pd.Series(ms_positions))
        
    return dist_df

# Algorithm
def create_env(foldername, nb_files = 10 ):
    list_files = listing_files(foldername)
    selected_files = list_files[:nb_files]
    dfs = read_files(selected_files)
    user_df = dfs[0]
    # print(user_df.head())
    df = get_all_distance(dfs, user_df)
    return df

df = create_env(foldername)
df.to_csv('illinois-env.csv', sep='|')


