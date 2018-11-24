#!/usr/bin/env python3

import pandas
from pandas import Series, DataFrame
from datetime import date
import sklearn.svm as sk
import sklearn.preprocessing as pre
from sklearn.model_selection import GridSearchCV
import matplotlib.pyplot as plt

holidays_2016 = ["2016-01-01", "2016-01-18", "2016-02-15", "2016-05-30", "2016-07-04", "2016-09-05", "2016-10-10", "2016-11-11", "2016-11-24", "2016-12-26"]
holidays_2017 = ["2017-01-01","2017-01-02", "2017-01-16", "2017-02-20", "2017-05-29", "2017-07-04", "2017-09-04", "2017-10-09", "2017-11-10", "2017-11-23", "2017-12-25"]


def main():
    #read in correct files
    filename = "2016-capitalbikeshare-tripdata/2016Q1-capitalbikeshare-tripdata.csv"
    file2= "2016-capitalbikeshare-tripdata/2016Q2-capitalbikeshare-tripdata.csv"
    file3= "2016-capitalbikeshare-tripdata/2016Q3-capitalbikeshare-tripdata.csv"
    file4= "2016-capitalbikeshare-tripdata/2016Q4-capitalbikeshare-tripdata.csv"
    testfile= "2017-capitalbikeshare-tripdata/2017Q1-capitalbikeshare-tripdata.csv"
    test2 = "2017-capitalbikeshare-tripdata/2017Q2-capitalbikeshare-tripdata.csv"
    test3 = "2017-capitalbikeshare-tripdata/2017Q3-capitalbikeshare-tripdata.csv"
    test4 = "2017-capitalbikeshare-tripdata/2017Q4-capitalbikeshare-tripdata.csv"
    
    #combine all the 2016 data and reset the index
    print("start")
    data = read_data(filename)
    data=data.append(read_data(file2))
    data=data.append(read_data(file3))
    data=data.append(read_data(file4))
    data=data.reset_index(drop=True)
    
    #REMOVE LATER: TAKES RANDOM SAMPLE OF THE DATA for speed if included
    data=data.sample(frac=0.25)
    data=data.sort_index()
    data=data.reset_index(drop=True)
    
    print("Raw Data in DataFrame")
    #adds day of week (as integer) and holiday (1 or 0) to the data
    data = map_data(data)
    #changes date format to include only the year-month-day for the start day
    data= drop_time(data)
    #remakes the dataframe so that the number of rides for each station each
    #day are summed and included as count (with other features stayng the same)
    data=date_as_obj(data)

    #included if want to graph the data it was fit too (NEED TO CHANGE THE PLOTTING FUNCITON)
    fitGraph=data
    #adds the feature month (1-12) to the data
    #Also adds the date as a number (should be 1-365 or something)
    #(??month may not be nexessary if including date???)
    data=month(data)
    #drop counts and date; date not used and counts will be used as Y in svr
    fitData=data.drop(["Counts", "Date"], axis=1)
    print("fit data ready")
    
    #Select data to test with the regressions
    
    #Support Vector Regression from skLearn
    print(fitData.head(10))
    
    #preprocessing from sklearn (suggested by SVR)
    #NOT SURE IF THIS COULD BE A PROBLEM WITH THE FIT (dont to fit and test
    #shouldnt skew stuff by maybe)
    print("preprocessing")
    scaler=pre.StandardScaler()
    fitData=scaler.fit_transform(fitData)
    fitData=DataFrame(fitData)
 
    print("Starting Grid Search SVR")
    #based on the tests I found this to be the best set of parameters but see below for
    #notes on the process
    model=sk.SVR(kernel='poly', degree=2, epsilon=0.75, gamma=1E-6, C=1E11, max_iter=50000)
    #paramToTest= {'degree':[2,3,5]}
    #best first time: gam=1E-5, C=1E8, poly, degree=2
    #search= GridSearchCV(model, paramToTest)
    #so far rbf got closest but still just a straight line over the parabola
    #For parameters: try GridSearchCV
    
    print("starting fit")
    #print("fit data \n", fitData)
    #print(fitData.head(5),data["Counts"].head(5))
    
    #fit the svr model
    model.fit(fitData, data["Counts"])
    
    pandas.set_option('display.max_columns', 500)
    #print(DataFrame(search.cv_results_))
    
    #do all the same stuff to the 2017 data as the 2016 data as test data
    print("formatting test data")
    testdata = read_data(testfile)
    testdata=testdata.append(read_data(test2))
    testdata=testdata.append(read_data(test3))
    testdata=testdata.append(read_data(test4))
    testdata=testdata.reset_index(drop=True)
    
    #REMOVE LATER: TAKES RANDOM SAMPLE OF THE DATA
    testdata=testdata.sample(frac=0.25)
    testdata=testdata.sort_index()
    testdata=testdata.reset_index(drop=True)
    
    testdata = map_data(testdata)
    testdata= drop_time(testdata)
    testdata=date_as_obj(testdata)
    testdata=month(testdata)
    testfit=testdata.drop(["Counts","Date"], axis=1)
    #preprocessing
    testfit=scaler.fit_transform(testfit)
    testfit=DataFrame(testfit)
    
    #predict, print prediction, plot
    print("starting predict")
    results=model.predict(testfit)
    results=DataFrame(results)
    print("Support Vector Regression")
    print(results.head(10))
    print("RMSE=", do_analysis(results, testdata))
    make_graph(testdata, results, fitGraph)
    return data

def read_data(name_file):
    dataframe = pandas.read_csv(name_file)
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
            vals.insert(1,"Holiday", temp.loc[temp["Date"]==first, "Holiday"].iloc[0])
            vals.insert(2,"Day of week", temp.loc[temp["Date"]==first, "Day of week"].iloc[0])
            newData=newData.append(vals)
            newData=newData.reset_index(drop=True)
    return newData

def month(allData):
    months=[]
    dateNum=[]
    days={}
    counter=0
    for i in allData['Date']:
        if i in days:
            dateNum.append(days[i])
        else:
            counter+=1
            days[i]=counter
            dateNum.append(days[i])
        year,month,day=i.split("-")
        months.append(month)
    allData['Month']=months
    allData['Date_num']=dateNum
    newDateData=allData[['Date_num', 'Start station number','Day of week','Holiday','Month','Date','Counts']].copy()
    newDateData=newDateData.reset_index(drop=True)
    return newDateData

def do_analysis(predict, actual):
    rmse= ((predict[0]-actual["Counts"])**2).mean() ** 0.5
    return rmse

def make_graph(actual, predict, fit):
    predict.columns=['SVR']
    whole = pandas.concat([actual, predict], axis=1)
    print(whole.head(10))
    whole= whole.loc[whole['Start station number'] == 31634]
    print("From Station 31634")
    print(whole.head(10))
    usegraph= whole.loc[:,['Date','Counts','SVR']]
    fitGraph=fit.loc[fit['Start station number']==31634]
    plt.scatter(usegraph['Date'], usegraph['Counts'], c='b', label="actual")
    plt.scatter(usegraph['Date'], usegraph['SVR'], c='g', label="Support Vector Regression")
    #if len(usegraph['Date'])>len(fitGraph['Counts']):
     #   plt.scatter(usegraph['Date'][0:len(fitGraph['Counts'])], fitGraph['Counts'], c='r', label="Fit Data")
    #else:
     #   plt.scatter(usegraph['Date'], fitGraph['Counts'][0:len(usegraph['Date'])], c='r', label="Fit Data")
    plt.legend()
    plt.savefig('svr_graph_withDates.png')
    

if __name__ == "__main__":
    main()
