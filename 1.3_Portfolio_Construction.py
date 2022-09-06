import pandas as pd
import numpy as np
import datetime
import yfinance as yf
import pickle
import matplotlib.pyplot as plt
import seaborn as sns
import quantstats as qs


with open('data/all_transformed_price_1-2.pickle','rb') as f:
    etf_price = pickle.load(f)

with open('data/etf_data.pickle','rb') as f:
    etf_data_org = pickle.load(f)

#=======================================================================#
#  Major Inputs:                                                        #
#  1. initial amount                                                    #
#  2. contribution_amount                                               #
#  3. contribution_freq = biweekly, monthly                             #
#                                                                       #
#                                                                       #
#  2. rebalance frequency: number of month                              #
#  3. rotation rule:                                                    #
#        rule 1: based on the growth rate, pure growth rate             #
#        rule 2:                                                        #
#        rule 3:                                                        #
#=======================================================================#

# initial_amount = 10_000
rebalance_freq = 3
rotation_rule = 1

class portfolio_sumulator:
    def __init__(self,initial_amount=10000,rebalance_freq=3, rule=1):
        self.initial = initial_amount
        self.rebalance_freq = rebalance_freq
        self.rule = rule
    def no_rebalance_direct_invest(self,ticker,start_date=20050101, end_date=20211031):
        stock_info = yf.download(ticker)
        initial_price =stock_info.loc[str(start_date):,'Adj Close'].values[0]
        initial_share = self.initial/initial_price
        end_price = stock_info.loc[:str(end_date),'Adj Close'].values[-1]
        end_value = end_price*initial_share
        print(f'Starting from {start_date}, end {end_date}, initial value is {self.initial}. the end value is {end_value}')
        return end_value
    def alpha_portfolio(self,start_date=20050901, end_date=20211231):
        start_date = pd.to_datetime(str(start_date))
        end_date = pd.to_datetime(str(end_date))
        # if self.rule == 1:
        #     rule_1()
        prior_start_date = start_date - pd.DateOffset(months=self.rebalance_freq)
        growth_performance_calculate = etf_price.loc[prior_start_date:start_date,:]
        growth_performance_calculate = growth_performance_calculate.iloc[-1,:]/growth_performance_calculate.iloc[0,:]-1
        growth_performance_calculate.drop('SPY_trans_price', inplace=True)
        growth_performance_calculate = growth_performance_calculate.nlargest(3)
        # TODO 1 what if all of them are negative

        # TODO 2 how to distribute the 30% amount. Now, it is the place holder， even distribute

        alpha_etfs = growth_performance_calculate.index.tolist()
        alpha_etfs = [x.split('_')[0] for x in alpha_etfs]

        #### Up to Here we can build the first portfolio setup =====
        spy_starting_price = etf_data_org['SPY'].loc[start_date: ,'Adj Close'].values[0]
        initial_spy_share = round(self.initial * 0.6 /spy_starting_price,2)




test=portfolio_sumulator()

test.no_rebalance_direct_invest('MSFT')

# extend pandas functionality with metrics, etc.
qs.extend_pandas()

# fetch the daily returns for a stock
stock = qs.utils.download_returns('META')

# show sharpe ratio
qs.stats.sharpe(stock)

qs.reports.basic(stock, "SPY")



'''
they are the same, daily return. 
stock = qs.utils.download_returns('META')
meta_price = yf.download('META')
meta_price['Adj Close'].pct_change(1)
'''










