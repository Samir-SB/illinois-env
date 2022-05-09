import numpy as np
import pandas as pd
# import haversine as hs
# from haversine import Unit
# import folium
# from os import listdir,  walk
# from os.path import isfile, join
import random
import utils


# plot all trajectories
def plot_all_trajectories(list_dfs, init_location):
    m = utils.build_map(init_location)
    colors = ['red', 'blue', 'green', 'orange', 'pink', 'black',
              'yellow', 'brown', 'corel', 'violet', 'indigo', 'teal']
    for df, color in zip(list_dfs, colors):
        # coordinates.dropna()
        utils.plot_trajectory(m, df.coordinate, color)

    m.save('map_mardi.html')


def load_data(folder_name):
    columns_label = ['Latitude', 'Longitude',
                     'time', 'x_projection', 'y_projection']
    columns_excluded = ['Latitude', 'Longitude', 'time',
                        'x_projection', 'y_projection']
    delimiter = '|'

    # 1. listing all files inside @folder_name
    # 2. choose only 10 columns (the first ten).
    selected_files = utils.listing_files(folder_name)[:10]

    list_dfs = []
    for filename in selected_files:
        df = pd.read_csv(filename, delimiter=delimiter)
        # add columns label
        df.columns = columns_label
        # exclude unecessary columns
        df.sort_values(by=['time'])

        # fix (Lat, Long) issue than tuple them in new columns
        df['coordinate'] = list(
            zip((df.Latitude / 100), (df.Longitude / (-100))))
        df = df.loc[:, ~df.columns.isin(columns_excluded)]

        list_dfs.append(df)
    return list_dfs


def calculate_distance_at(time):
    distance = 0
    for df in data:
        # find row conatais timestamp
        i = df[df['time'].str.contains(time)]

        if i.empty:
            # DataFrame is empty!
            distance = 100000
        else:
            # print(df.loc[df['time'].str.contains(time)])
            loc2 = i['coordinate'].values[0]
            distance = utils.distance_from(loc1, loc2)
        print(distance)


def calculate_all_distance(location, df):
    distance_df = df['coordinate'].apply(utils.distance_from, loc2=location)
    distance_df.values.tolist()

# ------------------------------------------
# start pgm --------------------------------
# @data is a list of dataframes
# each @df is : [time, coordinate]


# Algorithm
# load data
# select the first df as user_trajectory
# for each point inside user_trajectory
def algorithme():
    for id in range(9, 10):
        new_user_df = user_df['coordinate'].apply(
            calculate_all_distance, df=data[id])


# print(new_user_df.head())
#
data = load_data('dataset/custom/')
index1 = 5
index2 = 6
max_distance = 50
user_df = data[index1]

for loc1, loc2 in zip(user_df.coordinate, data[index2].coordinate):
    distance = utils.distance_from(loc1, loc2)
    print(distance)


# calculate distance
# user_location = user_df.coordinate[0]
# distance_df = calculate_all_distance(user_location, user_df)
# dft = distance_df[distance_df < max_distance]
# print(len(dft))


# -----
# user_loc = {
#   "ms1": {
#     "less_D:" [(coordinate, distance), ... ],
#     greater_D: [(coordinate, distance) ]
#   },
#   ms2: {
#     less_D: [(coordinate, distance) ]
#     greater_D: [(coordinate, distance) ]
#   }
# }