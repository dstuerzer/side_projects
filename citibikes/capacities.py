
import pandas as pd 
import matplotlib.pyplot as plt 
import numpy as np 
import random
import os
from scipy.misc import imread
import re
from sklearn import svm
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans, SpectralClustering
from sklearn.preprocessing import StandardScaler
import time
import matplotlib.colors as colors

import basic_functions as bf 
import plotting_functions as pf 

# this script plots the size of each station that would be required such that there are no shortages during the day
# (if there wasn't any redistribution of bikes)



# # weekdays in sep 2016
rainy_weekdays = ['01','09','14','19','27','30']
sunny_weekdays = ['02','04','05','06','07','08','12','13','15','16','20','21','22','23','26','28']
weekends = ['03','04','10','11','17','18','24','25']


date = '201609'
days = sunny_weekdays	#chose the kind of day




dt = 15

df, df_coor = bf.read_df(date)
df_start = df[df['starttime'].str[8:10].isin(days)]
df_stop = df[df['stoptime'].str[8:10].isin(days)]
dic_ = 	df_coor.set_index('id').T.to_dict('list')
dic_start = {}
dic_stop = {}
dic_freq = {}
dic_cumsum = {}
dic_capac = {}

for id in dic_:
	df_temp = df_start[df_start['start station id'] == id].loc[:,['starttime']]
	df_temp['starttime'] = df_temp['starttime'].apply(lambda x: x[-5:])
	dic_start[id] = bf.create_freq_list((df_temp.sort_values('starttime'))['starttime'].tolist(), dt, len(days))
	
	df_temp = df_stop[df_stop['end station id'] == id].loc[:,['stoptime']]
	df_temp['stoptime'] = df_temp['stoptime'].apply(lambda x: x[-5:])
	dic_stop[id] = bf.create_freq_list((df_temp.sort_values('stoptime'))['stoptime'].tolist(), dt, len(days))
	
	dic_freq[id] = bf.minus_li(dic_stop[id], dic_start[id])
	dic_cumsum[id] = np.cumsum(dic_freq[id])*dt/60
	dic_capac[id] = max(dic_cumsum[id]) - min(dic_cumsum[id])		#capacity

x,y,r = [], [], []
f = 4
for id in dic_capac:
	x.append(dic_[id][1])
	y.append(dic_[id][0])
	r.append(dic_capac[id]*f)
x,y,r = bf.reorder(x,y,r)
pf.plot_fun_2(x, y, r, '_'+date+'-size.png', 'green', f)
