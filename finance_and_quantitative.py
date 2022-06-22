# This program will show you how to compute portfolio simple returns, 
# get daily returns & volatility..

from datetime import datetime
import numpy as np
import pandas as pd
import pandas_datareader as web
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')

# Get the stock symbols for the portfolio.
# FAANG.
stockSymbols = ['META', 'AMZN', 'AAPL', 'NFLX', 'GOOG']

# Get the stock starting date.
stockStartDate = '2013-01-01'

# Get todays date and format it in the form YYYY-mm-dd.
today = datetime.today().strftime('%Y-%m-%d')

print(today)

# Get the number of assets in the portfolio.
numAssets = len(stockSymbols)

print('You have ' + str(numAssets) + ' assets in your portfolio.')

def getMyPortfolio(stocks=stockSymbols, start=stockStartDate, end=today, col='Adj Close'):
  '''
    Create a function to get the stock prices in the portfolio.
  '''
  data = web.DataReader(stocks, data_source='yahoo', start=start, end=end)[col]
  return data

print('Getting the stock portfolio Adj. Close price')
my_stocks = getMyPortfolio(stockSymbols)

print(my_stocks)

def showGraph(stocks=stockSymbols, start=stockStartDate, end=today, col='Adj Close'):
  '''
    Create a function to visualize the portfolio.
    apt-get install python3-tk -y
  '''
  print('Creating a title for the portfolio.')
  title = 'Portfolio ' + col + ' Price History'

  print('Getting the stocks.')
  my_stocks = getMyPortfolio(stocks=stocks, start=start, end=end, col=col)

  print('Plotting the figure size.')
  plt.figure(figsize=(12.2, 4.5))

  print('Looping through each stock and plot the price.')
  for c in my_stocks.columns.values:
    plt.plot(my_stocks.index, my_stocks[c], label=c)
  plt.title(title)
  plt.xlabel('Date', fontsize=18)
  plt.ylabel(col + ' Price USD ($)', fontsize=18)
  plt.legend(my_stocks.columns.values, loc='upper left')
  plt.show()

print('Showing the adjusted close price for FAANG.')
showGraph(stockSymbols)

print('Calculating the simple returns.')
daily_simple_returns = my_stocks.pct_change(1)

print('Showing the daily simple returns.')
print('META 2013-01-03, 2013-01-02: (27.77 / 28) - 1 is how python is doing these calculations.')
print(daily_simple_returns)

print('Showing the stock correlation.')
print(daily_simple_returns.corr())

print('Showing the covariance matrix for simple returns.')
print(daily_simple_returns.cov())

print('Showing the variance (values match those previously printed).')
print(daily_simple_returns.var())

print('Printing the standard deviation for daily simple returns.')
print('The stock volatility:')
print('daily_simple_returns.std')

print('Visualizing the stock daily simple returns / volatility.')
plt.figure(figsize=(12, 4.5))

print('Looping through each stock and plot the simple returns.')
for c in daily_simple_returns.columns.values:
  plt.plot(daily_simple_returns.index, daily_simple_returns[c], lw=2, label=c)

print('Creating a legend.')
plt.legend(loc='upper right', fontsize=10)
plt.title('Volatility')
plt.ylabel('Daily Simple Returns')
plt.xlabel('Date')
plt.show()

print('Showing the mean of the daily simple return.')
dailyMeanSimpleReturns = daily_simple_returns.mean()

print('The daily simple mean returns:')
print(dailyMeanSimpleReturns)

print('Calculating the expected portfolio daily return.')
randomWeights = np.array([0.4, 0.1, 0.3, 0.1, 0.1]) # 40% FB, 10% AMZN, 30% AAPL, 10% NFLX, 10% GOOG
portfolioSimpleReturn = np.sum(dailyMeanSimpleReturns * randomWeights)

print('Printing the expected portfolio return.')
print('The daily expected portfolio return: ' + str(portfolioSimpleReturn))

print('Getting the yearly simple return.')
print('Expected annualised portfolio simple return: ' + str(portfolioSimpleReturn * 253))

print('Calculating the growth of the investment.')
dailyCumulSimpleReturn = (daily_simple_returns + 1).cumprod()

print('Showing the cumulative simple returns.')
print(dailyCumulSimpleReturn)

print('(period_1 + 1) * (period_2 + 1) * .. * (period_n + 1)')
print((daily_simple_returns['GOOG'][1] + 1) * (daily_simple_returns['GOOG'][2] + 1))

print('Visualizing the daily cumulative simple returns.')
plt.figure(figsize=(12.2, 4.5))
for c in dailyCumulSimpleReturn.columns.values:
  plt.plot(dailyCumulSimpleReturn.index, dailyMeanSimpleReturns[c], lw=2, label=c)
plt.legend(loc='upper left', fontsize=10)
plt.xlabel('Date')
plt.ylabel('Growth of $1 investment')
plt.title('Daily Cumulative Simple Returns')
plt.show()
