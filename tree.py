#!/usr/bin/env python3

import pandas
from matplotlib import pyplot as plt
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import AdaBoostRegressor
import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error
from math import sqrt

def main():
    df = pandas.read_csv("2016Q1")
    df = df.append(pandas.read_csv("2016Q2"))
    df = df.append(pandas.read_csv("2016Q3"))
    df = df.append(pandas.read_csv("2016Q4"))

    test = pandas.read_csv("2017Q1")
    test = test.append(pandas.read_csv("2017Q2"))
    test = test.append(pandas.read_csv("2017Q3"))
    test = test.append(pandas.read_csv("2017Q4"))
    #make_scatter(df)
    train_predict_1d(df, test)
    #train_predict_2d(df, test)
    return

def make_scatter(df):
    plt.figure(figsize=(8,6))
    plt.plot(df['Start station number'], df['Counts'], 'o')
    plt.xlabel('Station')
    plt.ylabel('Counts')
    plt.show()
    return

def train_predict_1d(df, test):
    regressor = DecisionTreeRegressor(max_depth=2)
    regressor.fit(np.array([df['Start station number']]).T, df['Counts'])
    
    xx = np.array([test['Start station number']]).T
    plt.figure(figsize=(8,6))
    plt.plot(df['Start station number'], df['Counts'], 'o', label='observation')
    plt.plot(xx, regressor.predict(xx), linewidth=4, alpha=.7, label='prediction')
    plt.xlabel('Station')
    plt.ylabel('Counts')
    plt.legend()
    #plt.show()

    print("RMSE")
    print(sqrt(mean_squared_error(test['Counts'], regressor.predict(xx))))
    return

def train_predict_2d(df, test):
    #regressor = AdaBoostRegressor(DecisionTreeRegressor(max_depth=10), n_estimators=50, loss="square")
    regressor = DecisionTreeRegressor()
    regressor.fit(df[['Start station number', 'Quarter']], df['Counts'])

    nx = 30
    ny = 30
    
    x_station = np.linspace(30800,32300, nx) 
    y_day = np.linspace(0, 3, ny)
    xx, yy = np.meshgrid(x_station, y_day)

    z_counts = regressor.predict(np.array([xx.flatten(), yy.flatten()]).T)
    zz = np.reshape(z_counts, (nx, ny))

    fig = plt.figure(figsize=(8, 8))
    plt.pcolormesh(x_station, y_day, zz, cmap=plt.cm.YlOrRd)
    plt.colorbar(label='bikes predicted') 
    #plt.scatter(test['Start station number'], test['Counts'], s=test['Counts']/25.0, c='g')
    plt.xlim(np.min(x_station), np.max(x_station))
    plt.ylim(np.min(y_day), np.max(y_day))
    plt.xlabel('Start station number')
    plt.ylabel('Quarter')
    #plt.show()
    #fig.savefig("2d_prediction_quarter")

    print("Mean Absolute Error")
    print(mean_absolute_error(test['Counts'], regressor.predict(test[['Start station number', 'Quarter']])))
    print("RMSE")
    print(sqrt(mean_squared_error(test['Counts'], regressor.predict(test[['Start station number', 'Quarter']]))))

    return

if __name__ == "__main__":
    main()
