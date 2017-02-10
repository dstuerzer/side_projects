
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




def main_routes(date, days, t_begin, t_end):

	df, df_coor = bf.read_df(date)
	df_start, df_stop = bf.start_stop(df, days, t_begin, t_end)

	dic_ = 	df_coor.set_index('id').T.to_dict('list')		# dic with keys 'id' and value "[lat, lon]"


	del dic_[3182]
	del dic_[3254]
	list_id = [i for i in dic_]
	X = []
	for id in list_id:
		dic_x = df_start[df_start['start station id'] == id]['end station id'].value_counts().to_dict()
		x = []
		for jd in list_id:
			if jd in dic_x:
				x.append(dic_x[jd])
			else:
				x.append(0)
		X.append(x)

	Y = np.add(X, np.transpose(X))

	N_top_N = 200
	min_lw = 0.01
	max_lw = 20
	min_col = -2
	max_col = 25

	top_N = [0 for i in range(N_top_N)]
	von_nach = [0 for i in range(N_top_N)]

	for i in range(len(Y)):
		for j in range(len(Y[0])):
			if j>=i:
				if Y[i][j]>min(top_N):
						ii = top_N.index(min(top_N))
						top_N[ii] = Y[i][j]
						von_nach[ii] = [list_id[i], list_id[j]]
	print(min(top_N))
	print(max(top_N))
	mxtN = ((10*max(top_N))//(len(days)*(int(t_end)-int(t_begin))))/20
	mntN = ((10*min(top_N))//(len(days)*(int(t_end)-int(t_begin))))/20
	mdtN = (mxtN + mntN)/2
	# top_N = [fkt(ya) for ya in top_N]
	k = (min_lw-max_lw)/(min(top_N)-max(top_N))
	d = (max_lw*min(top_N)-min_lw*max(top_N))/(min(top_N)-max(top_N))
	top_N = [k*j + d for j in top_N]

	a = [q[0] for q in von_nach]
	b = [q[1] for q in von_nach]
	a,b,top_N = bf.reorder_asc(a,b,top_N)
	von_nach = [[a[i], b[i]] for i in range(len(a))]
	x = [dic_[s][1] for s in list_id]
	y = [dic_[s][0] for s in list_id]
	img = imread("mapp.png")
	fig = plt.figure(figsize=(20,42))
	ax=fig.add_subplot(1,1,1)
	ax.imshow(img, zorder=-1, extent=[-74.0338, -73.91844, 40.6627, 40.81549])
	
	c_map = plt.cm.get_cmap('gist_heat')
	cNorm  = colors.Normalize(vmin=min_col, vmax=max_col)
	scalarmap=plt.cm.ScalarMappable(norm=cNorm, cmap=c_map)


	for i in range(N_top_N):
		ax.plot([dic_[von_nach[i][0]][1], dic_[von_nach[i][1]][1]+0.0001],[dic_[von_nach[i][0]][0], dic_[von_nach[i][1]][0]+0.0001], linewidth = top_N[i], color = scalarmap.to_rgba(top_N[i]), solid_capstyle="round", zorder = 2)
	ax.scatter(x, y, color='green', edgecolors='darkgreen', zorder = 1)
	ax.plot([0,1], [1,2], linewidth = max_lw, color = scalarmap.to_rgba(max_lw), label = str(mxtN)+' bikes/h')
	ax.plot([0,1], [1,2], linewidth = max_lw//2, color = scalarmap.to_rgba(max_lw//2), label =str(mdtN)+' bikes/h')
	ax.plot([0,1], [1,2], linewidth = 1, color = scalarmap.to_rgba(1), label =str(mntN)+' bikes/h')
	

	ax.axes.set_aspect (1.3) 
	ax.set_xlim([-74.0338, -73.91844])
	ax.set_ylim([40.6627, 40.81549])
	ax.legend(loc="upper left", fontsize=40,prop={'size':40})
	plt.savefig('top_'+str(N_top_N)+'tracks'+str(t_begin)+'-'+str(t_end)+'.png',bbox_inches='tight')


for hh in range(7):
	main_routes('201609',  sunny_weekdays, bf.mak_2_dig(3*hh+1), bf.mak_2_dig(3*hh+4))

