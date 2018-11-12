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

def main():
    path_2016 = './2016-capitalbikeshare-tripdata/'
    path_2017 = './2017-capitalbikeshare-tripdata/'
    bike_2016 = os.listdir(path_2016)
    bike_2017 = os.listdir(path_2017)
    data_2016 = [0] * 4
    ix = 0
    for i in bike_2016:
        data_2016[bike_2016.index(i)] = read_data.read_data(path_2016 + i)
        data_2016[bike_2016.index(i)] = read_data.map_data(data_2016[bike_2016.index(i)])
        ix = ix + 1
        print("loading ... " + str(ix) + "/4 2016 data")
    data_2017 = [0] * 4
    ix = 0
    for i in bike_2017:
        data_2017[bike_2017.index(i)] = read_data.read_data(path_2017 + i)
        data_2017[bike_2017.index(i)] = read_data.map_data(data_2017[bike_2017.index(i)])
        ix = ix + 1
        print("loading ... " + str(ix) + "/4 2017 data")

    full_data_2016 = pd.concat(data_2016)
    full_data_2017 = pd.concat(data_2017)
    full_cov_2016 = full_data_2016.cov()
    full_cov_2017 = full_data_2017.cov()

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

    print full_cov_2016
    print full_cov_2017

main()
