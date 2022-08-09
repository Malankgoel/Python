import pandas as pd
from pandas_datareader import data as pdr
import numpy as np
import datetime as dt
from scipy.stats import norm
import matplotlib.pyplot as plt

a = input("Ticker #1: ").upper()
b = input("Ticker #2: ").upper()
c = input("Ticker #3: ").upper()
d = input("Ticker #4: ").upper()
tickers = [a, b, c, d]

print()
w1 = float(input("Ticker Weight (in decimal) for " + a + ": "))
w2 = float(input("Ticker Weight (in decimal) for " + b + ": "))
w3 = float(input("Ticker Weight (in decimal) for " + c + ": "))
w4 = float(input("Ticker Weight (in decimal) for " + d + ": "))
weights = np.array([w1, w2, w3, w4])

print()
ini_inv = int(input("Total Investment Amount: "))

dataset = pdr.get_data_yahoo(tickers, start="2020-01-01", end=dt.date.today())['Close']
returns = dataset.pct_change()
returns.tail()

portfolio_mean = np.dot(returns.mean(), weights)
portfolio_sd = np.sqrt(weights.dot(returns.cov()).dot(weights))

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

for i in range(1, days+1):
    var = np.round(var_d1 * np.sqrt(i), 2)
print()
print("The portfolio, with " + str(inp*100) + "% confidence, will not incur losses greater than " + str(var) + "USD over a " + str(days) + " day period.")

graph = input("Do you want to plot the graph for the maximum loss over the time period (Y/N): ").upper()
if graph == "Y":
    plt.xlabel("Day #")
    plt.ylabel("Max portfolio loss (USD)")
    plt.title("Max portfolio loss (VaR) over the time period")
    plt.plot(var_ar, "r")
    plt.show()
print("Thank You!")

