#!/usr/bin/env python3

import pandas
from pandas import Series, DataFrame
from datetime import date
import sklearn.linear_model as skLm

def main():
    filename = "2016-capitalbikeshare-tripdata/2016Q1-capitalbikeshare-tripdata.csv"
    testfile= "2017-capitalbikeshare-tripdata/2017Q1-capitalbikeshare-tripdata.csv"
    data = read_data(filename)
    data = map_data(data)
    data= drop_time(data)
    data=date_as_obj(data)
    #print(data)
    fitData=data.drop(["Counts", "Date"], axis=1)
    #Select data to test with the regressions
    testdata = read_data(testfile)
    testdata = map_data(testdata)
    testdata= drop_time(testdata)
    testdata=date_as_obj(testdata)
    testfit=data.drop(["Counts", "Date"], axis=1)
    #Bayesian Ridge Regression from skLearn
    brr=skLm.BayesianRidge()
    brr.fit(fitData, data["Counts"])
    resultsBRR=brr.predict(testfit)
    resultsBRR=DataFrame(resultsBRR)
    #Ordinary Linear Regression from sklearn
    olr= skLm.LinearRegression()
    olr.fit(fitData, data["Counts"])
    resultsOLR=olr.predict(testfit)
    resultsOLR= DataFrame(resultsOLR)
    print(data.head(10))
    print(testdata.head(10))
    print("Bayesian Ridge Regression")
    print(resultsBRR.head(10))
    print("RMSE=", do_analysis(resultsBRR, testdata))
    print("Ordinary Linear Regression")
    print(resultsOLR.head(10))
    print("RMSE=", do_analysis(resultsOLR, testdata))
    return data

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
    count = 4
    month = 1
    day = 1
    #0 is monday, 6 is sunday
    #1/1/2016 is a friday, so start count at 4
    for i in data["Start date"]:
        newi = i.split(" ")
        newerI = newi[0].split("-")
        Days.append(date(int(newerI[0]), int(newerI[1]), int(newerI[2])).weekday())
    data["Day of week"] = Days
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
            newData=newData.append(vals)
            newData=newData.reset_index(drop=True)
    return newData
def do_analysis(predict, actual):
    rmse= ((predict[0]-actual["Counts"])**2).mean() ** 0.5
    return rmse

if __name__ == "__main__":
    main()
