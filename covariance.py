#!/usr/bin/env python2.7

# Capital Bikeshare
# CSE40647
# chi-squared / covariance

import read_data
import numpy as np
import os
from scipy import stats
import pandas as pd
from datetime import date
import matplotlib.pyplot as plt
import sys

def main():
    path_2016 = './2016-capitalbikeshare-tripdata/'
    # path_2017 = './2017-capitalbikeshare-tripdata/'
    bike_2016 = os.listdir(path_2016)
    # bike_2017 = os.listdir(path_2017)
    data_2016 = [0] * 4
    ix = 0
    for i in bike_2016:
        #data_2016[bike_2016.index(i)] = read_data.read_data(path_2016 + i)
        data_2016[bike_2016.index(i)] = quarters(path_2016 + i)
        data_2016[bike_2016.index(i)] = read_data.map_data(data_2016[bike_2016.index(i)])
        ix = ix + 1
        sys.stdout.write("\rloading ... %d/4 2016 data" % ix)
        sys.stdout.flush()
        #print("loading ... " + str(ix) + "/4 2016 data")
    # data_2017 = [0] * 4
    # ix = 0
    # for i in bike_2017:
    #     data_2017[bike_2017.index(i)] = read_data.read_data(path_2017 + i)
    #     data_2017[bike_2017.index(i)] = read_data.map_data(data_2017[bike_2017.index(i)])
    #     ix = ix + 1
    #     print("loading ... " + str(ix) + "/4 2017 data")

    full_data_2016 = pd.concat(data_2016)

    # counts_2016_dict = dict()
    # rides = full_data_2016.shape[0]
    # iter = 0
    #
    # sys.stdout.write("\r\033[K")
    #
    # for index, row in full_data_2016.iterrows():
    #     if row['Start station number'] in counts_2016_dict:
    #         counts_2016_dict[row['Start station number']] += 1
    #     else:
    #         counts_2016_dict[row['Start station number']] = 1
    #     iter += 1
    #     if iter % 5000 == 0:
    #         pct = float(iter)/float(rides)*100
    #         sys.stdout.write("\rloading ... %d%% rides" % pct)
    #         sys.stdout.flush()
    #         #print "loading ... " + str(iter) + "/" + str(stations) + " stations"
    # #print counts_2016_dict

    # full_data_2017 = pd.concat(data_2017)
    full_cov_2016 = full_data_2016.cov()
    # full_cov_2017 = full_data_2017.cov()
    full_corr_2016 = full_data_2016.corr(method='pearson')
    # full_corr_2017 = full_data_2017.corr(method='pearson')

    # cov_2016 = [0] * 4
    # chi_2016 = [0] * 4
    # ix = 0
    # for i in data_2016:
    #     cov_2016[ix] = i.cov()
    #     #chi_2016[ix] = stats.chisquare(i.values, axis=None)
    #     ix = ix + 1
    #     print("Done ... " + str(ix) + "/4 covariance for 2016")
    # cov_2017 = [0] * 4
    # chi_2017 = [0] * 4
    # ix = 0
    # for i in data_2017:
    #     cov_2017[ix] = i.cov()
    #     #chi_2017[ix] = stats.chisquare(i.values, axis=None)
    #     ix = ix + 1
    #     print("Done ... " + str(ix) + "/4 covariance for 2017")
    # #print chi_2017
    # #print stats.chisquare(data_2017[1].values)

    print '\n2016 covariance'
    print full_cov_2016
    print '\n2016 correlation'
    print full_corr_2016

    # print '\n2017'
    # print full_cov_2017
    # print full_corr_2017

def quarters(name_file):
    dataframe = pd.read_csv(name_file)
    if 'Q1' in name_file:
        dataframe["Quarter"]=1
    elif 'Q2' in name_file:
        dataframe["Quarter"]=2
    elif 'Q3' in name_file:
        dataframe["Quarter"]=3
    elif 'Q4' in name_file:
        dataframe["Quarter"]=4
    dataframe.drop(["Member type", "Duration", "Bike number", "Start station", "End station", "End station number"], axis=1, inplace=True)
    return dataframe

main()
