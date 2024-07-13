import pandas as pd
import numpy as np
import yfinance as yf
import datetime

class Portfolio(object):

    def __init__(self, Tickers, Weights, Start_Date, End_Date,Investment):
        self._Tickers = Tickers
        self._Weights = Weights
        self._Start_Date = Start_Date
        self._End_Date = End_Date
        self._Investment = Investment

    @property
    def Tickers(self):
        return self._Tickers
    
    @Tickers.setter
    def Tickers(self, Tickers_list):
        self._Tickers = Tickers_list

    @property
    def Weights(self):
        return self._Weights
    
    @Weights.setter
    def Weights(self, Weights_list):
        self._Tickers = Weights_list

    def Weights_dict(self):
        return dict(zip(self._Tickers, self._Weights))


    @property
    def Start_Date(self):
        return self._Start_Date
    
    @Start_Date.setter
    def Start_Date(self, date):
        self._Start_Date = date
    
    @property
    def End_Date(self):
        return self._End_Date
    
    @End_Date.setter
    def End_Date(self, date):
        self._End_Date = date

    @property
    def Investment(self):
        return self._Investment
    
    @Investment.setter
    def Investment(self, investment):
        self._Investment = investment

    def GetPrices(self):

        df = pd.DataFrame()

        for Ticker in self.Tickers:

            Stock = yf.Ticker(Ticker)
            prices = Stock.history(start=self.Start_Date, end=self.End_Date)['Close']
            df[Ticker] = prices

        return df
    
    def GetPortValue(self,prices_df):

        if prices_df is None:
            prices_df = self.GetPrices()

        weighted_prices_df = prices_df * self.Weights

        portfolio_values = weighted_prices_df.sum(axis=1)

        daily_returns = portfolio_values.pct_change().fillna(0)
        initial_investment = self.Investment
        # Initialize the investment values DataFrame
        investment_values = pd.Series(index=portfolio_values.index, dtype=float)
        investment_values.iloc[0] = initial_investment

        # Calculate the investment value over time
        for i in range(1, len(daily_returns)):
            investment_values.iloc[i] = investment_values.iloc[i-1] * (1 + daily_returns.iloc[i])

        return investment_values
    
    def End_value(self, prices_df, weights):

        if prices_df is None and weights is None:
            port_Value = self.GetPortValue()
        else:
            weighted_prices_df = prices_df * self.Weights
            portfolio_values = weighted_prices_df.sum(axis=1)



        


        


    

