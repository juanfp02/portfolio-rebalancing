import pandas as pd
import numpy as np

def Statistics(portfolio, risk_free_rate):

    total_return = (portfolio.iloc[-1]/portfolio.iloc[1])-1
    total_count = len(portfolio)


    annualized_return = (1+total_return)**(365/total_count)-1

    daily_returns = portfolio.pct_change()

    daily_vol = np.std(daily_returns)

    annualized_vol = np.sqrt(252)*daily_vol

    sharpe = (annualized_return - risk_free_rate)/annualized_vol

    return [annualized_return,annualized_vol,sharpe]




def calculate_max_drawdown(prices):

    price_series = prices.iloc[:,0]
    
    peak = price_series[0]
    max_drawdown = 0
    
    # Loop through the price series to find the maximum drawdown
    for price in price_series:
        if price > peak:
            peak = price 
        drawdown = (peak - price) / peak
        if drawdown > max_drawdown:
            max_drawdown = drawdown 
    
    return max_drawdown  #


def main():
      
    pt = pd.DataFrame(pd.read_csv('Sell_Winners_Buy_Losers_freq12.csv', index_col=0))


    stats = Statistics(pt,0.0419)
    MDD = calculate_max_drawdown(pt)

    print(f"Annualized Return {stats[0]}")
    print(f"Annualized Volatility {stats[1]}")
    print(f"Sharpe Ratio {stats[2]}")
    
    print(f"Max Drawdown {MDD}")


if __name__ == '__main__':
      main()




