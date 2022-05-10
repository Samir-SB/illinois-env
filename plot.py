import pandas as pd
import matplotlib as plt
import json

def plot_distance(ms):
    # ms_1 = df['ms-1'].distance    
    new_df = pd.DataFrame(list(ms))
    new_df = new_df[new_df.distance < 1000]
    new_df.plot(y="distance", use_index=True, c='red')
    

def plot_all_distance(dfs, df):
    for i in range(1, len(dfs)):
        print(i)    
        # print(df.iloc[:, i].dropna())
        plot_distance(df.iloc[:, i].dropna())

# FIXME #https://stackoverflow.com/questions/22483588/how-can-i-plot-separate-pandas-dataframes-as-subplots
def plot(list_dataframes, colors):    
    for df, color in zip(list_dataframes, colors):
        df.plot(x="Longitude", y="Latitude", c=color)  


def get_mservice_by_id(id):
  return df[id]

def get_state_by_step(step):
  return df.iloc[step]

def format_state(state):
  my_dict = state.to_dict()
  if 'Unnamed: 0' in my_dict:
    del my_dict['Unnamed: 0']
  return my_dict

def format_state_2(state):
    return state[1:].to_dict()

def  extract_long_lat(state):
  return state
  
## ___________________________________________________________________ ##

df = pd.read_csv('illinois-env.csv', delimiter='|')
#print(df.head())


ms = get_mservice_by_id('ms-1')
# print(ms.head())

state = get_state_by_step(150)
# print(state)

   
    
# df_transposed = state.T
# df_transposed[["Longitude", "Latitude"]] = pd.DataFrame(df_transposed[2:].position.tolist(), index= df_transposed.index)
# df_transposed.to_csv('state.csv')
   
     
  
df_state = extract_long_lat(state) 
print(df_state) 
  
# df_transposed.plot.scatter(x="Longitude", y="Latitude", c="blue")



# ms_trajectory = pd.DataFrame(list(ms)).position
# plot_distance(ms)
# plt.show()

    #https://pandas.pydata.org/pandas-docs/version/0.25.0/reference/api/pandas.DataFrame.plot.scatter.html

