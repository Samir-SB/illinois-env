import numpy as np
import pandas as pd
# import haversine as hs
# from haversine import Unit
# import folium
# from os import listdir,  walk
# from os.path import isfile, join
import random
import utils2
class env():
  def __init__(self, action_space = 10, D = 50):
    self.D = D
    self.step = 0
    self.action_space = action_space  
    
  def set_step(self, step):
    self.step = step
   
  
  def load_data(self, files, columns_label, columns_excluded):
    data = []
    for filename in files:
      df = pd.read_csv(filename, delimiter='|')
      # add columns label
      df.columns = columns_label
      # exclude unecessary columns
      df = df.loc[:, ~df.columns.isin(columns_excluded)]         
      data.append(df)
    return data
  
  def preprocessing_data(self, data):
    processing_data = pd.DataFrame([])
    for df in data:      
      df['coordinate'] = list(zip((df.Latitude /100), (df.Longitude /(-100))))
      columns_nb = len(processing_data.columns)
      processing_data.insert(columns_nb , f't-{columns_nb + 1}', df.coordinate)
    return processing_data
  
# create an environment
  def build_env(self, randomly = False):
    columns_label = ['Latitude', 'Longitude', 'time','x_projection', 'y_projection' ]
    columns_excluded = ['x_projection', 'y_projection']
    list_files = utils2.listing_files('dataset/person1')
    if (randomly):
      files = random.sample(list_files,  self.action_space)       
    else:
      files = list_files[:10]
    processing_data = self.preprocessing_data(self.load_data(files, columns_label, columns_excluded))
    # replace NaN values with 0
    # processing_data = processing_data.fillna(0)
    self.user_trajectory = processing_data['t-1'].dropna()
    self.ms_trajectories = processing_data.drop(['t-1'], axis=1)
    self.state_space = len(self.user_trajectory)
  

  # initialize the environment
  def reset_env(self):  
    self.step = 0
    # return position(lat, long ) of user
    return self.user_trajectory[self.step]  

  # calculate reward.........
  def calculate_reward(self, i_action):
    user_coordinate = self.user_trajectory.iloc[self.step] 
    ms_coordinate = self.ms_trajectories.iloc[self.step, i_action]  
    distance = utils2.distance_from(user_coordinate, ms_coordinate)
    if (distance > self.D ):
      return -10
    return np.random.rand()

  def step(self, i_action, stepp = 1):
    #return next_state, reward, done, _
    reward = self.calculate_reward(i_action)
    self.step = self.step + stepp
    done = (self.step == self.state_space)
    next_state = self.user_trajectory[self.step]
    return (next_state, reward, done )  


  def render(self):
    pass
  
  def render_state(self, map):
    print(self.step)
    utils2.add_circleMarker(map, self.user_trajectory[self.step], self.D)
    print( self.ms_trajectories.shape)
    for position in self.ms_trajectories.iloc[self.step]:
      if( position != position):
        print ('-----')
      else:
        print(position)
        utils2.add_circleMarker(map, position, self.D, color ='blue')