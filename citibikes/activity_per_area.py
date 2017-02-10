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


def where_to_from(date, days, t_begin, t_end):
	# days has to be a list of 2-digit strings
	# times have to be 2-digit strings each, representing the hour, eg. '09' stands for 09:00
	#
	# plots stations to which bikes go that leave a specific station, and
	# plots stations where bikes come from that arrive at a spec. station
	df, df_coor = bf.read_df(date)
	df_start, df_stop = bf.start_stop(df, days, t_begin, t_end)

	frequent_starts = df_start['start station id'].value_counts().nlargest(3).to_dict()
	frequent_stops = df_stop['end station id'].value_counts().nlargest(3).to_dict()

	dic_ = 	df_coor.set_index('id').T.to_dict('list')		# dic with keys 'id' and value "[lat, lon]"

	f = 50
	for id in frequent_starts:
		dic_to = df_start[df_start['start station id'] == id]['end station id'].value_counts().to_dict()
		x_minus, y_minus, r_minus = [dic_[id][1]], [dic_[id][0]], [(f*frequent_starts[id])//((int(t_end)-int(t_begin))*len(days))]
		x_plus, y_plus, r_plus = [], [], []
		for di in dic_to:
			x_plus.append(dic_[di][1])
			y_plus.append(dic_[di][0])
			r_plus.append((dic_to[di]*f)//((int(t_end)-int(t_begin))*len(days)))
		pf.plot_diff_3(x_plus, y_plus, r_plus, x_minus, y_minus, r_minus, '_'+date+'-'+t_begin+'-'+t_end+'-von-'+str(id)+'.png', 'Goals of bikes starting at station '+str(id), f, 'green')
	
	for id in frequent_stops:
		dic_to = df_stop[df_stop['end station id'] == id]['start station id'].value_counts().to_dict()
		x_plus, y_plus, r_plus = [dic_[id][1]], [dic_[id][0]], [(f*frequent_stops[id])//((int(t_end)-int(t_begin))*len(days))]
		x_minus, y_minus, r_minus = [], [], []
		for di in dic_to:
			x_minus.append(dic_[di][1])
			y_minus.append(dic_[di][0])
			r_minus.append((dic_to[di]*f)//((int(t_end)-int(t_begin))*len(days)))
		pf.plot_diff_3(x_plus, y_plus, r_plus, x_minus, y_minus, r_minus, '_'+date+'-'+t_begin+'-'+t_end+'-nach-'+str(id)+'.png', 'Origin of bikes going to station '+str(id), f, 'red')

def where_to_from_area(date, days, t_begin, t_end):
	#basically the same as where_to_from, but with starting/destination AREAS
	# some selected rectangles below:

	# penn station
	# lat_range = [40.745, 40.765]
	# lon_range = [-74.003, -73.993]

	# east village
	# lat_range = [40.714, 40.733]
	# lon_range = [-73.987, -73.972]

	# # midtown
	# lat_range = [40.755, 40.767]
	# lon_range = [-73.987, -73.976]

	#financial district
	lat_range = [40.7005, 40.716]
	lon_range = [-74.0142, -74.0027]



	df, df_coor = bf.read_df(date)
	df_start, df_stop = bf.start_stop(df, days, t_begin, t_end)

	# create coord dict named "dic_"

	ids_restricted = df_coor[(df_coor['lat'] > lat_range[0]) & (df_coor['lat'] < lat_range[1]) & (df_coor['lon']>lon_range[0]) & (df_coor['lon'] < lon_range[1])]['id'].tolist()
	dic_ = 	df_coor.set_index('id').T.to_dict('list')		# dic with keys 'id' and value "[lat, lon]"

	# df_start are those startig at the right time, and
	# df_stop are those stopping at the right time
	df_start = df_start[df_start['start station id'].isin(ids_restricted)]

	start_freqs_start = df_start['start station id'].value_counts().to_dict()
	stop_freqs_start = df_start['end station id'].value_counts().to_dict()

	df_stop = df_stop[df_stop['end station id'].isin(ids_restricted)]

	start_freqs_stop = df_stop['start station id'].value_counts().to_dict()
	stop_freqs_stop = df_stop['end station id'].value_counts().to_dict()

	f = 20	#Multiplikator zur Groeszenanpassung in den Plots

	x_minus, y_minus, r_minus = [], [], []		#start-Punkte
	for id_start in start_freqs_start:
		x_minus.append(dic_[id_start][1])
		y_minus.append(dic_[id_start][0])
		r_minus.append((start_freqs_start[id_start]*f)//((int(t_end)-int(t_begin))*len(days)))
	
	x_plus, y_plus, r_plus = [], [], []
	for id_stop in stop_freqs_start:
		x_plus.append(dic_[id_stop][1])
		y_plus.append(dic_[id_stop][0])
		r_plus.append((stop_freqs_start[id_stop]*f)//((int(t_end)-int(t_begin))*len(days)))


	x_minus, y_minus, r_minus = bf.reorder(x_minus, y_minus, r_minus)
	x_plus, y_plus, r_plus = bf.reorder(x_plus, y_plus, r_plus)
	pf.plot_diff_3(x_plus, y_plus, r_plus, x_minus, y_minus, r_minus, '__'+date+'-'+t_begin+'-'+t_end+'start_restricted.png', "Average net activity per hour", f, 'green')


	x_minus, y_minus, r_minus = [], [], []
	for id_start in start_freqs_stop:
		x_minus.append(dic_[id_start][1])
		y_minus.append(dic_[id_start][0])
		r_minus.append((start_freqs_stop[id_start]*f)//((int(t_end)-int(t_begin))*len(days)))
	
	x_plus, y_plus, r_plus = [], [], []
	for id_stop in stop_freqs_stop:
		x_plus.append(dic_[id_stop][1])
		y_plus.append(dic_[id_stop][0])
		r_plus.append((stop_freqs_stop[id_stop]*f)//((int(t_end)-int(t_begin))*len(days)))
	x_minus, y_minus, r_minus = bf.reorder(x_minus, y_minus, r_minus)
	x_plus, y_plus, r_plus = bf.reorder(x_plus, y_plus, r_plus)
	pf.plot_diff_3(x_plus, y_plus, r_plus, x_minus, y_minus, r_minus, '__'+date+'-'+t_begin+'-'+t_end+'stop_restricted.png', "Average net activity per hour", f, 'red')


where_to_from('201609',  rainy_weekdays, '19', '21')
where_to_from_area('201609',  sunny_weekdays, '07', '10')