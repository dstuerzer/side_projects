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

def plot_stations(date):
# visualizes all stations over a map
	script_dir = os.path.dirname(__file__) 
	rel_path = "Data/"+date+"_stat_coor.csv"
	abs_file_path = os.path.join(script_dir, rel_path)
	df = pd.read_csv(abs_file_path, encoding='latin-1')
	x = df['lon'].tolist()
	y = df['lat'].tolist()
	img = imread("mapp.png")
	fig = plt.figure(figsize=(10,21))
	ax=fig.add_subplot(1,1,1)
	ax.axes.set_aspect (1.25) 
	ax.scatter(x, y, color='green', edgecolors='darkgreen')
	ax.imshow(img, zorder=0, extent=[-74.0338, -73.91844, 40.6627, 40.81549])	
	plt.show()

def plot_diff_3(x_plus, y_plus, r_plus, x_minus, y_minus, r_minus, nae, titl, f, ord):
	img = imread("mapp.png")
	fig = plt.figure(figsize=(13,21))
	ax=fig.add_subplot(1,1,1)
	#green or red on top
	if ord == 'green':
		ax.scatter(x_minus, y_minus, s=r_minus, color='red', edgecolors='darkred')
		ax.scatter([5], [5], [2*f], color='red', label='-2 bikes', edgecolors='darkred')
		ax.scatter([5], [5], [10*f], color='red', label='-10 bikes', edgecolors='darkred')
		ax.scatter([5], [5], [50*f], color='red', label='-50 bikes', edgecolors='darkred')
		ax.scatter(x_plus, y_plus, s=r_plus, color='green', edgecolors='darkgreen')
		ax.scatter([5], [5], [2*f], color='green', label='2 bikes', edgecolors='darkgreen')
		ax.scatter([5], [5], [10*f], color='green', label='10 bikes', edgecolors='darkgreen')
		ax.scatter([5], [5], [50*f], color='green', label='50 bikes', edgecolors='darkgreen')
	else:
		ax.scatter(x_plus, y_plus, s=r_plus, color='green', edgecolors='darkgreen')
		ax.scatter([5], [5], [2*f], color='green', label='2 bikes', edgecolors='darkgreen')
		ax.scatter([5], [5], [10*f], color='green', label='10 bikes', edgecolors='darkgreen')
		ax.scatter([5], [5], [50*f], color='green', label='50 bikes', edgecolors='darkgreen')
		ax.scatter(x_minus, y_minus, s=r_minus, color='red', edgecolors='darkred')
		ax.scatter([5], [5], [2*f], color='red', label='-2 bikes', edgecolors='darkred')
		ax.scatter([5], [5], [10*f], color='red', label='-10 bikes', edgecolors='darkred')
		ax.scatter([5], [5], [50*f], color='red', label='-50 bikes', edgecolors='darkred')
	ax.imshow(img, zorder=0, extent=[-74.0338, -73.91844, 40.6627, 40.81549])
	ax.xaxis.set_ticklabels([])
	ax.yaxis.set_ticklabels([])
	ax.set_title(titl,fontsize=30)
	ax.legend(loc="upper left", scatterpoints=1, fontsize=20,prop={'size':20})
	ax.axes.set_aspect (1.3) 
	plt.savefig(nae,bbox_inches='tight')

def plot_fun(start_freqs, stop_freqs, dic_, t_begin, t_end, days, date, f):
#3 plots: starts, stops, and differences, colorcoded
# fi is a scaling factor for the scatter dots sizes, dic_ contains stat coor

	x,y,r = [], [], []
	for id in start_freqs:
		x.append(dic_[id][1])
		y.append(dic_[id][0])
		r.append((start_freqs[id]*f)//((int(t_end)-int(t_begin))*len(days)))
	x,y,r = bf.reorder(x,y,r)
	plot_fun_2(x, y, r, '_'+date+'-'+t_begin+'-'+t_end+'-start.png', 'red', f)

	x,y,r = [], [], []
	for id in stop_freqs:
		x.append(dic_[id][1])
		y.append(dic_[id][0])
		r.append((stop_freqs[id]*f)//((int(t_end)-int(t_begin))*len(days)))
	x,y,r = bf.reorder(x,y,r)
	plot_fun_2(x, y, r, '_'+date+'-'+t_begin+'-'+t_end+'-stop.png', 'green', f)

	### differenz - Teil
	f=10
	x,y,r = [],[],[]
	for id in start_freqs:
		x.append(dic_[id][1])
		y.append(dic_[id][0])
		if id in stop_freqs:
			r.append((f*(stop_freqs[id]-start_freqs[id]))//((int(t_end)-int(t_begin))*len(days)))
		else:
			r.append((f*(-start_freqs[id]))//((int(t_end)-int(t_begin))*len(days)))
	for id in stop_freqs:
		if id not in start_freqs:
			x.append(dic_[id][1])
			y.append(dic_[id][0])
			r.append((f*(stop_freqs[id]))//((int(t_end)-int(t_begin))*len(days)))

	x_minus, y_minus, r_minus, x_plus, y_plus, r_plus = [], [], [], [], [], []
	for i in range(len(r)):
		if r[i] >= 0:
			x_plus.append(x[i])
			y_plus.append(y[i])
			r_plus.append(r[i])
		else:
			x_minus.append(x[i])
			y_minus.append(y[i])
			r_minus.append(-r[i])

	x_plus, y_plus, r_plus = bf.reorder(x_plus, y_plus, r_plus)
	x_minus, y_minus, r_minus = bf.reorder(x_minus, y_minus, r_minus)
	# plot_diff_2(x_plus, y_plus, r_plus, x_minus, y_minus, r_minus, date+'-net-'+t_begin+'-'+t_end+'.png', f)
	plot_diff_3(x_plus, y_plus, r_plus, x_minus, y_minus, r_minus, '_'+date+'-'+t_begin+'-'+t_end+'-net_activity.png', 'Net activity per station', f, 'green')

def plot_fun_2(x,y,r, nae, col, f):
	if col == 'red':
		rere = 'Rents'
	else:
		rere = 'Returns'

	img = imread("mapp.png")
	fig = plt.figure(figsize=(13,21))
	ax=fig.add_subplot(1,1,1)
	ax.scatter(x, y, s=r, color=col, edgecolors='dark'+col)
	ax.scatter([5], [5], [2*f], color='green', label='2 '+"bikes", edgecolors='dark'+col)
	ax.scatter([5], [5], [10*f], color=col, label='10 '+"bikes", edgecolors='dark'+col)
	ax.scatter([5], [5], [50*f], color=col, label='50 '+"bikes", edgecolors='dark'+col)
	ax.imshow(img, zorder=0, extent=[-74.0338, -73.91844, 40.6627, 40.81549])
	ax.xaxis.set_ticklabels([])
	ax.yaxis.set_ticklabels([])

	ax.set_title(rere, fontsize=30)
	ax.legend(loc="upper left", scatterpoints=1, fontsize=20,prop={'size':20})
	ax.axes.set_aspect (1.3) 
	plt.savefig(nae,bbox_inches='tight')
