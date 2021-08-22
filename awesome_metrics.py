import numpy as np

def get_portfolio_allocation_and_valuation(portfolio_df, close_prices_df):
    """
    This function calculates the total value of a portfolio, as well as the 
    allocation of each security given the symbols, number of shares, 
    and prices of each asset.

    Arguments:
    portfolio_df: a dataframe containing at least 2 columns (none of them in the index), called: 'symbol', 'quantity'.
                  'symbol' should contain the ticker, cusip, or identifier of the security
                  'quantity' should contain the amount of units of the individual securities, such as the number of shares, 
                  for which the price is given.
    
    close_price_df: a dataframe containing the time series of close prices, with the more current price at the end, with 
                    columns sorted in the same order than the 'symbol' columns of the portfolio_df

    Returns:
    The original dataframe extended with 3 columns:
        1. the price of each security,
        2. the total value of each position, and 
        3. the allocation on each position
    """
    # Getting last prices  
    last_price = []
    for t in portfolio_df['symbol']:
        last_price.append(close_prices_df[t]['close'][-1])

    portfolio_df['price'] = last_price
    portfolio_df['total'] = portfolio_df['price'] * portfolio_df['quantity']


    portfolio_df['Allocation'] = portfolio_df['total'] /portfolio_df['total'].sum()
    total_portfolio_valuation=portfolio_df['total'].sum()

    return([portfolio_df, total_portfolio_valuation])



def get_annual_expected_return_volatility_and_sharpe_ratio(portfolio_weights, portfolio_daily_returns):
    """
    This function returns an array of the following key metrics of a portfolio:  
    annualized expected return, volatility, and sharpe ratio.
    
    Arguments:
    portfolio_weights: a list with the allocation of the individual securities of the portfolio
    portfolio_daily_returns: a DataFrame with the daily returns of each of the securities
    in the portfolio, in the same orden than the portfolio_weights

    Returns:
    An array with the following float calculations:
        expected annual return, 
        portfolio annualized volatility, 
        annualized portfolio sharpe ratio
    """
    portfolio_weights = np.array(portfolio_weights)
    
    #Annual expected return by the weighted average of the historical average of daily returns of each security, multiplied by 252
    expected_annual_return = np.sum(portfolio_daily_returns.mean() * portfolio_weights) * 252
    
    # Annual Portfolio Variance = w.T * Covariance * w    (where "*" represents here the matrix multiplication) OBS: Var_annual = Var_daily * 252
    # np.dot function does a matrix multiplication. Another alternative is np.matmul
    portfolio_variance = np.dot( portfolio_weights.T,   np.dot(   portfolio_daily_returns.cov() * 252, portfolio_weights   ))
    portfolio_volatility = np.sqrt(portfolio_variance)

    #Sharpe Ratio (annual) (Assumed risk_free_rate=0)
    risk_free_rate_annualized=0
    sharpe_ratio = (expected_annual_return - risk_free_rate_annualized)/portfolio_volatility
    
    return np.array([expected_annual_return,portfolio_volatility,sharpe_ratio]) 
