#!/usr/bin/env python3

import pandas
from matplotlib import pyplot as plt
from sklearn.tree import DecisionTreeRegressor
import numpy as np
from sklearn.metrics import mean_absolute_error

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
    #train_predict_1d(df)
    train_predict_2d(df, test)
    return

def make_scatter(df):
    plt.figure(figsize=(8,6))
    plt.plot(df['Start station number'], df['Counts'], 'o')
    plt.xlabel('Station')
    plt.ylabel('Counts')
    plt.show()
    return

def train_predict_1d(df):
    regressor = DecisionTreeRegressor(max_depth=2)
    regressor.fit(np.array([df['Start station number']]).T, df['Counts'])
    
    xx = np.array([df['Start station number']]).T
    plt.figure(figsize=(8,6))
    plt.plot(df['Start station number'], df['Counts'], 'o', label='observation')
    plt.plot(xx, regressor.predict(xx), linewidth=4, alpha=.7, label='prediction')
    plt.xlabel('Station')
    plt.ylabel('Counts')
    plt.legend()
    plt.show()
    return

def train_predict_2d(df, test):
    regressor = DecisionTreeRegressor(max_depth=4)
    regressor.fit(df[['Quarter', 'Day of week']], df['Counts'])

    nx = 30
    ny = 30
    
    x_station = np.linspace(0,3, nx) 
    y_day = np.linspace(0, 6, ny)
    xx, yy = np.meshgrid(x_station, y_day)

    z_counts = regressor.predict(np.array([xx.flatten(), yy.flatten()]).T)
    zz = np.reshape(z_counts, (nx, ny))

    fig = plt.figure(figsize=(8, 8))
    plt.pcolormesh(x_station, y_day, zz, cmap=plt.cm.YlOrRd)
    plt.colorbar(label='bikes predicted') 
    plt.scatter(test['Quarter'], test['Counts'], s=test['Counts']/25.0, c='g')
    plt.xlim(np.min(x_station), np.max(x_station))
    plt.ylim(np.min(y_day), np.max(y_day))
    plt.xlabel('Quarter')
    plt.ylabel('Day of Week')
    #plt.show()
    #fig.savefig("2d_prediction_quarter")

    print(mean_absolute_error(test['Counts'], regressor.predict(test[['Quarter', 'Day of week']])))

    return

if __name__ == "__main__":
    main()