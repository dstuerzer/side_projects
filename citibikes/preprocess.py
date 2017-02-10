import pandas as pd 
import numpy as np 
import os
import re
import basic_functions as bf

#reads every month's file into a csv containing the bike station information, and one containing the trip information
#this is to make later processing easier
#for every month all stations with their coordinates are written into one file

date_begin = ['2015', '01']
date_end = ['2016', '09']

script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
date = ''.join(date_begin)
date_end_str = ''.join(date_end)
while date <= date_end_str:
	rel_path = "Data/"+date+"-citibike-tripdata.csv"
	abs_file_path = os.path.join(script_dir, rel_path)
	df = pd.read_csv(abs_file_path)
	del df['tripduration']
	df['starttime'] = df['starttime'].apply(lambda x: bf.date_time(x))	#replace dates into my format
	df['stoptime'] = df['stoptime'].apply(lambda x: bf.date_time(x))
	# read station information -> df_stop
	df_stop = df.loc[:, ['start station id', 'start station name', 'start station latitude', 'start station longitude','end station id', 'end station name', 'end station latitude', 'end station longitude']]
	# keep rental information -> df
	df.drop(['usertype', 'start station name', 'start station latitude', 'start station longitude','end station name', 'end station latitude', 'end station longitude'], axis = 1, inplace = True)

	# write rental info (df) to csv. only station ids are kept
	rel_path = "Data/"+date+".csv"
	abs_file_path = os.path.join(script_dir, rel_path)
	df.to_csv(abs_file_path, index = False)
	# extract station informations. distinguish between start and stop stations, and merge them later 
	df_start = df_stop.loc[:, ['start station id', 'start station latitude', 'start station longitude']]
	df_stop.drop(['start station id', 'start station name', 'start station latitude', 'start station longitude',  'start station name',  'end station name'], axis = 1, inplace = True)
	df_start.columns = ['id', 'lat', 'lon']
	df_stop.columns = ['id', 'lat', 'lon']
	df = pd.concat([df_start, df_stop])
	df.drop_duplicates(inplace = True)

	ids = df["id"]
	multiple_stations = df[ids.isin(ids[ids.duplicated()])]
	#check whether start and stop ids always correspond to the same adress/location
	if len(multiple_stations['id'].tolist()) > 0:
		print('WARNING: ids not consistent for'+date)
		print(multiple_stations)

	rel_path = "Data/"+date+"_stat_coor.csv"
	abs_file_path = os.path.join(script_dir, rel_path)
	df.to_csv(abs_file_path, index = False)	
	print("coordinates written for "+date)
	date = bf.date_plus_1(date)