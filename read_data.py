#!/usr/bin/env python3

import pandas
from pandas import Series, DataFrame

def main():
    filename = "2016-capitalbikeshare-tripdata/2016Q1-capitalbikeshare-tripdata.csv"
    data = read_data(filename)
    return data

def read_data(name_file):
    dataframe = pandas.read_csv(name_file)
    dataframe.drop(["Member type", "Duration", "Bike number", "Start station", "End station"], axis=1, inplace=True)
    return dataframe

if __name__ == "__main__":
    main()