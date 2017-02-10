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





# # weekdays in sep 2016
rainy_weekdays = ['01','09','14','19','27','30']
sunny_weekdays = ['02','04','05','06','07','08','12','13','15','16','20','21','22','23','26','28']
weekends = ['03','04','10','11','17','18','24','25']

# 1. PLOTS FOR ALL DAY


date = '201609'
days = sunny_weekdays	#choose the kind of day


df, df_coor = bf.read_df(date)
df_start = df[df['starttime'].str[8:10].isin(days)]
df_stop = df[df['stoptime'].str[8:10].isin(days)]
dic_ = 	df_coor.set_index('id').T.to_dict('list')		# dic with keys 'id' and value "[lat, lon]"
start_freqs = df_start['start station id'].value_counts().to_dict()
stop_freqs = df_stop['end station id'].value_counts().to_dict()
pf.plot_fun(start_freqs, stop_freqs, dic_, '00', '24', days, date, 30)


# 2. TIME-SPECIFIC PLOTS

t_begin = '16'
t_end = '19'

# days has to be a list of 2-digit strings
# times have to be 2-digit strings each, representing the hour, eg. '09' stands for 09:00
df_start, df_stop = bf.start_stop(df, days, t_begin, t_end)
dic_ = 	df_coor.set_index('id').T.to_dict('list')		# dic with keys 'id' and value "[lat, lon]"

start_freqs = df_start['start station id'].value_counts().to_dict()
stop_freqs = df_stop['end station id'].value_counts().to_dict()
pf.plot_fun(start_freqs, stop_freqs, dic_, t_begin, t_end, days, date, 10)