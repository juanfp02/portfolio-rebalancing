import pandas as pd
import numpy as np
import yfinance as yf
import datetime
from Portfolio import Portfolio


def weight_generator(tickers):
    nb_tickers = len(tickers)

    return np.random.dirichlet(np.ones(nb_tickers), size=1)[0]

def MarkowitzOptimalPortfolio(tickers, simulations, start_date, end_date, risk_free_rate):

    results = []

    portfolio_prices = pd.DataFrame()
    weights = []

    pt = Portfolio(tickers, weights, start_date, end_date, None)
    prices_df = pt.GetPrices()

    for i in range(simulations):
        random_weights = weight_generator(tickers)  # You need to define weight_generator function

        pt = Portfolio(tickers, random_weights, start_date, end_date, None)

        stats = pt.GetPortfStatistics(prices_df,random_weights,risk_free_rate)

        # Extracting required statistics
        annualized_return = stats[0]
        annualized_volatility = stats[1]
        sharpe = stats[2]

        # Storing weights of each ticker
        weights_dict = pt.Weights_dict()

        # Constructing a dictionary for the current portfolio's results
        portfolio_result = {
            "Portfolio Number": i + 1,
            "Annualized Return": annualized_return,
            "Annualized Volatility": annualized_volatility,
            "Sharpe Ratio": sharpe,
            **weights_dict  # Unpacking weights dictionary
        }

        results.append(portfolio_result)

    # Creating DataFrame from results
    df = pd.DataFrame(results)

    # Reordering columns
    columns_order = ["Portfolio Number", "Annualized Return", "Annualized Volatility", "Sharpe Ratio"]
    tickers_order = sorted(tickers)  # Sort tickers alphabetically
    columns_order.extend(tickers_order)  # Add tickers to column order
    df = df[columns_order]


    Max_sharpe_portfolio = df.iloc[df["Sharpe Ratio"].idxmax()]
    Max_return_portfolio = df.iloc[df["Annualized Return"].idxmax()]
    Min_variance_portfolio = df.iloc[df["Annualized Volatility"].idxmin()]

    result_portfolios_dict = {"Max Sharpe Portfolio": Max_sharpe_portfolio,"Max Return Portfolio":Max_return_portfolio, "Min Variance Portfolio": Min_variance_portfolio}

    return result_portfolios_dict


def extract_weights(portfolio_dict):
    # Convert the dictionary to a list of tuples (key, value)
    items = list(portfolio_dict.items())
    
    # Extract the weights starting from the 5th element onwards
    weights = [value for key, value in items[4:]]
    
    return weights


def Date_list(start_date, end_date, interval):


    # Convert start_date and end_date to pandas datetime objects
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)

    # Initialize the list of dates with the start date
    dates = [start_date]

    # Generate intermediate dates by adding one month at a time
    current_date = start_date
    while current_date < end_date:
        current_date = current_date + pd.DateOffset(months=interval)
        if current_date < end_date:
            dates.append(current_date)

    # Add the end date
    dates.append(end_date)

    return dates

    
 

def Backtest(start_date, end_date, tickers, strategy, frequency, initial_investment, nb_simulations, risk_free_rate):

    dates_list = Date_list(start_date, end_date,frequency)
    periods = len(dates_list)
    complete_port = pd.DataFrame()

    #1st case: Markowitz optimal portfolio strategies
    if strategy == 'Max Sharpe Portfolio' or strategy == 'Min Variance Portfolio' or strategy == 'Max Return Portfolio':

        #Define the starting weights in the portfolio
        start_date = pd.to_datetime(start_date)
        debut_date = start_date - pd.DateOffset(months=frequency)

        initial_weights = extract_weights(MarkowitzOptimalPortfolio(tickers,nb_simulations,debut_date,end_date, risk_free_rate)[strategy])

        #Readjustment loop

        for i in range(1, periods):
            print(f"iteration {i} de {periods}")

            #define the iterating dates
            begin_date = dates_list[i-1]
            finish_date = dates_list[i]

            if i == 1:
                pt = Portfolio(tickers,initial_weights,begin_date,finish_date,initial_investment)
                port_value = pt.GetPortValue(None)
                new_weights = initial_weights
                investment = port_value.iloc[-1]

            else:
                previous_begin_date = dates_list[i-2]
                new_weights = extract_weights(MarkowitzOptimalPortfolio(tickers,nb_simulations,previous_begin_date,begin_date,0)[strategy])
                pt = Portfolio(tickers,new_weights,begin_date,finish_date,investment)
                port_value = pt.GetPortValue(None)

                investment = port_value.iloc[-1]
            
            complete_port = pd.concat([complete_port, port_value], ignore_index=True)

    elif strategy == 'Sell winners buy losers':


        initial_weights = [1/len(tickers)]*len(tickers)
        investment = initial_investment
        for i in range(1,periods):
            print(f"iteration {i} de {periods}")

            begin_date = dates_list[i-1]
            finish_date = dates_list[i]

            pt = Portfolio(tickers, initial_weights,begin_date,finish_date,investment)
            port_value = pt.GetPortValue(None)

            investment = port_value.iloc[-1]
            complete_port = pd.concat([complete_port, port_value], ignore_index=True)

    
    return complete_port


def calculate_max_drawdown(df, value_column=0):
        """
        Calculate the maximum drawdown of a portfolio.

        Parameters:
        df (pd.DataFrame): DataFrame containing daily portfolio values.
        value_column (str): Column name for portfolio values.

        Returns:
        float: The maximum drawdown as a decimal.
        """
        # Ensure the DataFrame is sorted by date
        df = df.sort_index()

        # Calculate the daily returns
        df['DailyReturn'] = df[value_column].pct_change()

        # Calculate the cumulative returns
        df['CumulativeReturn'] = (1 + df['DailyReturn']).cumprod()

        # Calculate the running maximum of the cumulative returns
        df['RunningMax'] = df['CumulativeReturn'].cummax()

        # Calculate the drawdown
        df['Drawdown'] = df['CumulativeReturn'] / df['RunningMax'] - 1

        # Calculate the maximum drawdown
        max_drawdown = df['Drawdown'].min()

        return max_drawdown


    


         
