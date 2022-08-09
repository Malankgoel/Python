import pandas as pd
from pandas_datareader import data as pdr
import numpy as np
import datetime as dt
from scipy.stats import norm
import matplotlib.pyplot as plt

num = int(input("How many tickers do you want? "))
tickers = []
for i in range(num):
    a = input("Ticker #" + str(i+1) + ": ").upper()
    tickers.append(a)

print()
while True:
    weights = []
    for i in range(num):
        w = float(input("Ticker Weight (in decimal) for " + tickers[i] + ": "))
        weights.append(w)
    if sum(weights) == 1:
        break
    else:
        print()
        print('The weights should add up to 1')
weights = np.asarray(weights)

print()
ini_inv = int(input("Total Investment Amount: "))

dataset = pdr.get_data_yahoo(tickers, start="2018-01-01", end=dt.date.today())['Close']
returns = dataset.pct_change()
returns.tail()

portfolio_mean = returns.mean().dot(weights)
portfolio_sd = np.sqrt(weights.T.dot(returns.cov()).dot(weights))

investment_mean = (1 + portfolio_mean) * ini_inv
investment_sd = ini_inv * portfolio_sd

print()
inp = float(input("Confidence Level (in decimal): "))
conf = 1 - inp
cut = norm.ppf(conf, investment_mean, investment_sd)

print()
var_d1 = ini_inv - cut
print('The portfolio, with ' + str(inp*100) + '% confidence, will not incur losses greater than ' + str(var_d1.round(2)) + "USD over a one day period.")

print()
days = int(input("Time Period (in days): "))
var_ar = []
var = 0
for i in range(1, days+1):
    var_ar.append(np.round(var_d1 * np.sqrt(i), 2))

var = np.round(var_d1 * np.sqrt(days), 2)
print()
print("The portfolio, with " + str(inp*100) + "% confidence, will not incur losses greater than " + str(var) + "USD over a " + str(days) + " day period.")

print()
graph = input("Do you want to plot the graph for the maximum loss over the time period (Y/N): ").upper()
if graph == "Y":
    plt.xlabel("Day #")
    plt.ylabel("Max portfolio loss (USD)")
    plt.title("Max portfolio loss (VaR) over the time period")
    plt.plot(var_ar, "r")
    plt.show()
print()
print("Thank You!")
