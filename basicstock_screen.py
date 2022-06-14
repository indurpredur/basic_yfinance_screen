#   program screens and analyzes stock data


# import libraries
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
import numpy as np
from datetime import date
import sys
#variable for # of companies user wants to analyze
print("")
number = int(input("ENTER INTEGER FOR NUMBER OF COMPANIES FOR ANALYSIS : "))

# Define the interval of interest, year 2021 to today
today = date.today()
start_date = '2021-01-01'
end_date = today

# define a dataframe
data_single_choice = pd.DataFrame()
i=0
#loop for number of analysis
while i < number:
    #input valid ticker for choice
    choice = input("Please enter a valid ticker: ")
    print("analyzing choice:", choice)
    print("")

    # get the data from the "yahoo" data source
    data_single_choice = yf.download(choice
                                     , start=start_date
                                     , end=end_date
                                     )
    #add ticker column and name rows with the name of the ticker (choice)   &   remove adj close column
    data_single_choice['Ticker'] = choice
    data_single_choice = data_single_choice.drop(columns='Adj Close')

    print(choice," filtered df")
    print(data_single_choice)
    print("")

    print(choice, " df info")
    print(data_single_choice.info())
    print("")

    print(choice," df stats (mean of Close should match year_avg in choice 1)")
    print(data_single_choice.describe())
    print("")


    #choice for user to make for analysis
    analyze = int(input("1: dataframe over/under avg \n2: 20 day sma with chart \nEnter integer 1 or 2: "))
    print("")
    if analyze ==1:

        print("dataframe of",choice,"flagged below or above yearly average close")
        #year_avg column will be the mean of all the close prices
        data_single_choice['year_avg'] = data_single_choice["Close"].mean()
        #flag column will be ABOVEavg if close > year_avg and BELOWavg if not
        data_single_choice['flag'] = np.where(data_single_choice['Close'] > data_single_choice['year_avg'],"++ABOVEavg", "--BELOWavg")

        print(data_single_choice[['Close','year_avg','flag']])

        print("End of",choice," analysis")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("---NEXT ANALYSIS---")

    if analyze == 2:
        # calculate the simple moving average SMA
        # SMA over a rolling window of 20 and 50 days
        sma_20d = 20
        sma_50d = 50
        df_stock_sma_20days = data_single_choice.rolling(sma_20d).mean()
        # rename all columns to add the suffix 'sma_20d'
        df_stock_sma_20days = df_stock_sma_20days.add_suffix('_sma20d')

        df_stock_sma_50days = data_single_choice.rolling(sma_50d).mean()
        # rename all columns to add the suffix 'sma_50d'
        df_stock_sma_50days = df_stock_sma_50days.add_suffix('_sma50d')


        close = data_single_choice[['Close']]
        # merge the original close values with sma_20d
        df_stock_close_vs_sma = pd.merge(close, df_stock_sma_20days, left_index=True, right_index=True)
        # merge new merged data(close with sma20) with with sma50d for multi sma
        df_stock_close_vs_sma2 = pd.merge(df_stock_close_vs_sma, df_stock_sma_50days, left_index=True, right_index=True)

        print("50sma vs 20sma vs close ")
        print(df_stock_close_vs_sma2[['Close','Close_sma20d', 'Close_sma50d']])

        # plot the open Vs close values by date (date is the index of the dataframe)
        df_stock_close_vs_sma2[['Close', 'Close_sma20d', 'Close_sma50d']].plot()
        #title is ticker in choice variable
        plt.title(choice)
        plt.show()

        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("---NEXT ANALYSIS---")

    i+=1
    if i == number:
        print(number," tickers were analyzed")
