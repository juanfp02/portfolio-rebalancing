from Portfolio import Portfolio
from Functions import MarkowitzOptimalPortfolio, extract_weights, Date_list, Backtest, calculate_max_drawdown
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
import datetime





def main():


    start_date = '2019-01-01'
    end_date = '2024-07-01'

    rebalancing_interval = 12 #in months

    tickers = ['IUES.L', 'IUMS.L', 'IUIS.L', 'IUCD.L', 'IUCS.L', 'IUFS.L', 'IUHC.L', 'IUIT.L', 'IUCM.L', 'IUUS.L']
    weights = [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]

    dates_list = Date_list(start_date, end_date,rebalancing_interval)
    periods = len(dates_list)

    df = Backtest(start_date, end_date, tickers, 'Max Sharpe Portfolio',rebalancing_interval,1000,1000,0.0419)

    df.to_csv('####.csv')
    

if __name__ == '__main__':
    main()

