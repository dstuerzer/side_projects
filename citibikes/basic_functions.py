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

def read_df(date):
	#read out the travel history and the station list
	script_dir = os.path.dirname(__file__) 
	rel_path = "Data/"+date+".csv"
	abs_file_path = os.path.join(script_dir, rel_path)
	rel_path_2 = "Data/"+date+"_stat_coor.csv"
	abs_file_path_2 = os.path.join(script_dir, rel_path_2)
	return pd.read_csv(abs_file_path, encoding='latin-1'), pd.read_csv(abs_file_path_2, encoding='latin-1')

def mak_2_dig(x):
#transforms any integer between 0 and 99 into a 2-digit string
	if x<10:
		return('0'+str(x))
	else:
		return(str(x))

def date_time(s):
#transforms time from datasets into convenient format (lex. sortable)
	if not '/' in s:
		ne=re.split("-| |:",s)
		tim=[mak_2_dig(int(i)) for i in ne]
	else:
		ne=re.split("/| |:",s)
		tim=[mak_2_dig(int(i)) for i in ne]
		tim[0], tim[1], tim[2] = tim[2],tim[0],tim[1]
	return tim[0]+'-'+tim[1]+'-'+tim[2]+'-'+tim[3]+'-'+tim[4]#+'-'+tim[5] 	save only in minutes


def date_plus_1(date):
# date incrementation block; from one month to the next.
	yy = int(date[:4])
	mo = int(date[4:])
	if mo == 12:
		yy+=1
	mo = (mo % 12) +1
	return str(yy)+mak_2_dig(mo)

#reorder functions with respect to the third column
def reorder(x,y,r):
	df_temp = pd.DataFrame({'A': x ,'B': y ,'C': r})
	df_temp = df_temp.sort_values(['C'], ascending=[False])
	return df_temp['A'].tolist(), df_temp['B'].tolist(), df_temp['C'].tolist()

def reorder_asc(x,y,r):
	df_temp = pd.DataFrame({'A': x ,'B': y ,'C': r})
	df_temp = df_temp.sort_values(['C'], ascending=[True])
	return df_temp['A'].tolist(), df_temp['B'].tolist(), df_temp['C'].tolist()

def start_stop(df, days, t_begin, t_end):

	df_start = df[df['starttime'].str[8:10].isin(days)]
	df_start = df_start[ (df_start['starttime'].str[11:13]>=t_begin) & (df_start['starttime'].str[11:13]<t_end)]
	df_stop = df[df['stoptime'].str[8:10].isin(days)]
	df_stop = df_stop[ (df_stop['stoptime'].str[11:13]>=t_begin) & (df_stop['stoptime'].str[11:13]<t_end)]
	return df_start, df_stop

def add_dt(s, dt):
	t = int(s[-2:])
	t +=dt
	if t>=60:
		h = 1
		t = t%60
	else:
		h=0

	hh = mak_2_dig(int(s[:2])+h)
	mm = mak_2_dig(t)
	return hh+'-'+mm

def create_freq_list(lis, dt, no_days):
	# lis needs to be lists of strings in the format 'hh-mm', sorted already
	# dt is the size of time steps in minutes
	# t = add_dt('00-00', dt)
	ls = []
	i = 0
	t = '00-00'
	while t<'24-00':
		t = add_dt(t, dt)
		ls.append(0)
		if i<len(lis):
			while lis[i]<t:
				ls[-1] += 60/(no_days*dt)
				i+=1
				if i == len(lis):
					break
	return ls

def minus_li(lp, lm):
#difference of 2 lists, lp-lm
	lu = []
	if len(lp) == len(lm):
		for i in range(len(lp)):
			lu.append(lp[i] - lm[i])
	else:
		print('Error')
	return lu