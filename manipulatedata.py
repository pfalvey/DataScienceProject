#!/usr/bin/env python3

import pandas
from pandas import Series, DataFrame
from datetime import date

holidays_2016 = ["2016-01-01", "2016-01-18", "2016-02-15", "2016-05-30", "2016-07-04", "2016-09-05", "2016-10-10", "2016-11-11", "2016-11-24", "2016-12-26"]
holidays_2017 = ["2017-01-02", "2017-01-16", "2017-02-20", "2017-05-29", "2017-07-04", "2017-09-04", "2017-10-09", "2017-11-10", "2017-11-23", "2017-12-25"]

def main():
    filename = "2017-capitalbikeshare-tripdata/2017Q4-capitalbikeshare-tripdata.csv"
    data = read_data(filename)
    data = map_data(data)
    data = drop_time(data)
    data = date_as_obj(data)
    data.to_csv("2017Q4")
    return 

def read_data(name_file):
    dataframe = pandas.read_csv(name_file)
    if 'Q1' in name_file:
        dataframe["Quarter"]=1
    elif 'Q2' in name_file:
        dataframe["Quarter"]=2
    elif 'Q3' in name_file:
        dataframe["Quarter"]=3
    elif 'Q4' in name_file:
        dataframe["Quarter"]=4
    dataframe.drop(["Member type", "Duration", "Bike number", "Start station", "End station"], axis=1, inplace=True)
    return dataframe

def map_data(data):
    Days = []
    Holidays = []
    count = 4
    month = 1
    day = 1
    #0 is monday, 6 is sunday
    #1/1/2016 is a friday, so start count at 4
    for i in data["Start date"]:
        newi = i.split(" ")
        newerI = newi[0].split("-")
        Days.append(date(int(newerI[0]), int(newerI[1]), int(newerI[2])).weekday())
        if newi[0] in holidays_2016:
            Holidays.append(1)
        else:
            Holidays.append(0)
    data["Day of week"] = Days
    data["Holiday"] = Holidays
    return data

def drop_time(data):
    date = []
    to_drop = []
    for index, row in data.iterrows():
        if row["Start date"].split()[0]== row["End date"].split()[0]:
            date.append(row["Start date"].split()[0])
        else:
            to_drop.append(index)
    data.drop(["Start date", "End date"], axis=1, inplace=True)
    data.drop(data.index[to_drop], inplace=True)
    data["Date"] = date
    return data

def date_as_obj(data):
    first=0
    newData=DataFrame()
    for i in data['Date']:
        if i!=first:
            first=i
            temp=data.loc[data['Date']==first]
            vals=DataFrame(temp["Start station number"].value_counts())
            vals=vals.reset_index()
            vals.columns=["Start station number", "Counts"]
            vals.insert(0, "Date", first)
            vals.insert(1,"Day of week", temp.loc[temp["Date"]==first, "Day of week"].iloc[0])
            vals.insert(2,"Quarter", temp.loc[temp["Date"]==first, "Quarter"].iloc[0])
            vals.insert(3, "Holiday", temp.loc[temp["Date"]==first, "Holiday"].iloc[0])
            newData=newData.append(vals)
            newData=newData.reset_index(drop=True)
    return newData

if __name__ == "__main__":
    main()