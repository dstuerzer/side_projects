
This repo contains the code which I have written to create the results dicsussed at dstuerzer.github.io/website/citi_bikes.html

## Setup


1. Download the data from https://s3.amazonaws.com/tripdata/index.html into a folder ./Data relative to the code.
2. Run preprocess.py. This will take a couple of minutes, while the files are processed into a workable format.

## Modules


### basic_functions.py

Contains all 'technical' functions used throughout the code.

### plotting_functions.py

Contains the different functions used for displaying the data.

### daily_net_activity.py

1. Plots number of starts and stops per station and day, and the difference
2. Plots the number of starts, stops and their difference per station, for a given time interval (eg. rush hours)

### activity_per_area.py

You can select either the n most active stations, and see where the bikes come from, or where they go to from this station.
Or you can select a rectangle on the map (via coordinates) and see where the bikes come from that arrive within
this rectangle, or where bikes starting in this rectangle go to.

### capacities.py

Shows for every station the difference between maximum and minimum number of bikes stationed in the station. This 
number is the minimum number of bikes necessary to be stationed in order to satisfy the daily demand.

### classification_of_profiles.py

Profiles vary from station to station. A big distinction can be made between stations active in the morning
and those active in the evening. K-means clustering is applied to the station profiles.

### main_connections.py

A first impression on the routes of higher activity. For every pair of stations, a connecting line is drawn, with
a width proportional to the average number of bikes going between those stations. This should visualize
active routes.
