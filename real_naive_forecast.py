#!/usr/bin/env python3

import pandas
from pandas import Series, DataFrame
from sklearn.metrics import mean_squared_error
from math import sqrt

def main():
    test = pandas.read_csv("2017Q1")
    test = test.append(pandas.read_csv("2017Q2"))
    test = test.append(pandas.read_csv("2017Q3"))
    test = test.append(pandas.read_csv("2017Q4"))
    predicted = naive_forecast(test)
    print("RMSE")
    print(sqrt(mean_squared_error(predicted["Actual Count"], predicted["Predicted Count"])))

def naive_forecast(data):
    date_station = {}
    for index, row in data.iterrows():
        if row["Date"] not in date_station:
            date_station[row["Date"]] = {}
        date_station[row["Date"]][row["Start station number"]] = row["Counts"]
    
    days = []
    actual = []
    pred = []
    stations = []
    
    i = 0
    for day in date_station.keys():
        j = 0
        total = 0
        for station, count in date_station[day].items():
            days.append(day)
            actual.append(count)
            stations.append(station)
            j += 1
            total += count
        avg = total/j
        for station, count in date_station[day].items():
            if i == 0:
                pred.append(0)
            elif i != 365:
                pred.append(avg)
        i += 1
    
    predicted = pandas.DataFrame()
    predicted["Date"] = days
    predicted["Station"] = stations
    predicted["Predicted Count"] = pred
    predicted["Actual Count"] = actual
    #print(len(days))
    #print(len(stations))
    #print(len(pred))
    #print(len(actual))
    
    return predicted

if __name__ == "__main__":
    main()