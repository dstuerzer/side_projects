
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


date = '201609'
days = sunny_weekdays	#chose the kind of day



df, df_coor = bf.read_df(date)
df_start = df[df['starttime'].str[8:10].isin(days)]
df_stop = df[df['stoptime'].str[8:10].isin(days)]
dic_ = 	df_coor.set_index('id').T.to_dict('list')
dic_start = {}
dic_stop = {}
dic_freq = {}
dic_cumsum = {}
dt = 30
X = []
i = 0
dic_rel = {}
for id in dic_:
	df_temp = df_start[df_start['start station id'] == id].loc[:,['starttime']]
	df_temp['starttime'] = df_temp['starttime'].apply(lambda x: x[-5:])
	dic_start[id] = bf.create_freq_list((df_temp.sort_values('starttime'))['starttime'].tolist(), dt, len(days))
	
	df_temp = df_stop[df_stop['end station id'] == id].loc[:,['stoptime']]
	df_temp['stoptime'] = df_temp['stoptime'].apply(lambda x: x[-5:])
	dic_stop[id] = bf.create_freq_list((df_temp.sort_values('stoptime'))['stoptime'].tolist(), dt, len(days))
	
	dic_freq[id] = bf.minus_li(dic_stop[id], dic_start[id])
	dic_cumsum[id] = np.cumsum(dic_freq[id])*dt/60
	x = dic_freq[id]		# the dict to be used for classification
	if np.std(x) > 0:
		# x = [s - x[0] for s in x]
		x = x/np.std(x)
		X.append(x)
		dic_rel[id] = x
		# X.append(x)

k_cluster=2		#number of clusters

pca = PCA(n_components=2, whiten=True)	#pca dimension reduction no1 for reduced kmeans
# pca = StandardScaler()
pca.fit(X)
Y=pca.transform(X)

KM = KMeans(n_clusters=k_cluster)	#Kmeans for reduced data
KM.fit(Y)		#make fit
cc = KM.cluster_centers_
Z=KM.predict(Y)	#apply prediction to data df
M = pca.inverse_transform(cc)
# name_cmap = 'seismic'
name_cmap = 'bwr'
c_map = plt.cm.get_cmap(name_cmap)
cNorm  = colors.Normalize(vmin=0, vmax=max(set(Z)))
scalarmap=plt.cm.ScalarMappable(norm=cNorm, cmap=c_map)
red_center_y=KM.predict(cc)
coo=scalarmap.to_rgba(red_center_y)


xax = np.arange(0,24,dt/60)
f, (ax2, ax3) = plt.subplots(1,2, sharey=False)
i = 0
for m in M:
	ax2.plot(xax, m, c=coo[i])
	i+=1
ax3.scatter(Y[:,0], Y[:,1], c=Z,lw=0, cmap=c_map)
ax3.xaxis.set_ticklabels([])
ax3.yaxis.set_ticklabels([])
ax2.set_xlim([0, 24])
ax2.set_xlabel('Time (h)')
plt.savefig('clusters.png',bbox_inches='tight')
plt.close()

x = []
y = []
z = []
for id in dic_rel:
	x.append(dic_[id][1])
	y.append(dic_[id][0])
	z.append(dic_rel[id])
z = KM.predict(pca.transform(z))

img = imread("mapp.png")
fig = plt.figure(figsize=(13,21))
ax=fig.add_subplot(1,1,1)
ax.scatter(x, y, s=150, c=z, lw = 0, cmap=c_map)
for j in z:
	ax.scatter([5], [5], c=j)
ax.imshow(img, zorder=0, extent=[-74.0338, -73.91844, 40.6627, 40.81549])
ax.xaxis.set_ticklabels([])
ax.yaxis.set_ticklabels([])
ax.legend(loc="upper left", scatterpoints=1, fontsize=20,prop={'size':20})
ax.axes.set_aspect (1.3) 
plt.savefig('kmeans.png',bbox_inches='tight')
