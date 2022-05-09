import numpy as np
import pandas as pd
import haversine as hs
from haversine import Unit
import folium
from os import listdir,  walk
from os.path import isfile, join
import random

def listing_files(foldername):  
  data_files = []
  for root, directories, files in walk(foldername, topdown=False):
      for name in files:
          filename = join(root, name)
          data_files.append(filename)
  return data_files

def build_map(initial_coordinate):
  initial_position = list(initial_coordinate)
  m = folium.Map(location=initial_position, zoom_start=250, width='99%')
  tooltip = 'starting position'
  folium.Marker(initial_position, popup="<i>initial position</i>", tooltip=tooltip).add_to(m)
  return m

def add_marker(map, position):
  folium.Marker(position, popup="<i>initial position</i>", tooltip='tooltip').add_to(map)
  
def add_circleMarker(map, position, radius, color = 'red'):
  folium.CircleMarker(
            location=position,
            radius=radius,
            popup= 'this is popup',
            color=color,
            fill=True,
            fill_color= color
            ).add_to(map) 

def plot_trajectory(map, trajectory, color='blue', ):
  folium.PolyLine(trajectory, color=color).add_to(map)

def plot_ms_trajctories(map, ms_trajectories):
  colors = ['red', 'blue', 'green', 'orange', 'pink', 'black', 'yellow', 'brown', 'corel', 'violet', 'indigo', 'teal']
  for traj, color in zip(ms_trajectories, colors):
    ms_traj = ms_trajectories[traj].dropna()    
    plot_trajectory(map, ms_traj, color=color)
    
def distance_from(loc1,loc2):
    #To calculate distance in meters 
      dist=hs.haversine(loc1,loc2,unit=Unit.METERS)
      return round(dist,2)