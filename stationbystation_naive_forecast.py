#!/usr/bin/env python3

import pandas
from pandas import Series, DataFrame

def naive_forecast(data):
    date_station = {}
    for index, row in data.iterrows():
        if row["Date"] not in date_station:
            date_station[row["Date"]] = {}
        date_station[row["Date"]][row["Start station number"]] = row["Counts"]
    
    days = []
    stations = []
    locations = []
    actual = []
    pred = []
    for station in date_station['2016-01-01'].keys():
        stations.append(station)
    for station in stations:
        i = 0
        predictions = []
        for day, dictionary in date_station.items():
            for location, count_value in dictionary.items():
                if location == station:
                    if i <1:
                        predictions.append(count_value)
                    actual.append(count_value)
                    days.append(day)
                    locations.append(station)
                    predictions.append(count_value)
            i+=1
        del predictions[-1]
        for value in predictions:
            pred.append(value)
        print(len(predictions))
        print(len(actual))
        print(i)
        print(len(pred))
    predicted = pandas.DataFrame()
    predicted["Date"] = days
    predicted["Station"] = locations
    predicted["Predicted Count"] = pred
    predicted["Actual Count"] = actual
    return predicted
