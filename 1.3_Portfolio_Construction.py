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
    def __init__(self, initial_amount=10000, rebalance_freq=3, rule=1):
        self.initial = initial_amount
        self.rebalance_freq = rebalance_freq
        self.rule = rule

    def no_rebalance_direct_invest(self, ticker, start_date=20050101, end_date=20211031):
        stock_info = yf.download(ticker)
        initial_price = stock_info.loc[str(start_date):, 'Adj Close'].values[0]
        initial_share = self.initial / initial_price
        end_price = stock_info.loc[:str(end_date), 'Adj Close'].values[-1]
        end_value = end_price * initial_share
        print(
            f'Starting from {start_date}, end {end_date}, initial value is {self.initial}. the end value is {end_value}')
        return end_value

    def alpha_portfolio(self, start_date=20050901, end_date=20211231, spy_weight=0.6):
        start_date = pd.to_datetime(str(start_date))
        end_date = pd.to_datetime(str(end_date))
        # if self.rule == 1:
        #     rule_1()
        prior_start_date = start_date - pd.DateOffset(months=self.rebalance_freq)
        growth_performance_calculate = etf_price.loc[prior_start_date:start_date, :]
        growth_performance_calculate = growth_performance_calculate.iloc[-1, :] / growth_performance_calculate.iloc[0,
                                                                                  :] - 1
        growth_performance_calculate.drop('SPY_trans_price', inplace=True)
        growth_performance_calculate = growth_performance_calculate.nlargest(3)
        # TODO 1 what if all of them are negative

        # TODO 2 how to distribute the 30% amount. Now, it is the place holder， even distribute

        alpha_etfs = growth_performance_calculate.index.tolist()
        alpha_etfs = [x.split('_')[0] for x in alpha_etfs]

        #### Up to Here we can build the first portfolio setup =====
        portfolio_df = pd.DataFrame(index=etf_price.loc[start_date:end_date, :].index)

        spy_starting_price = etf_data_org['SPY'].loc[start_date:, 'Adj Close'].values[0]
        initial_spy_share = round(self.initial * spy_weight / spy_starting_price, 2)
        ## for each alpha ETFs
        each_portion_money = self.initial * (1 - spy_weight) / len(alpha_etfs)
        alpha_etfs_shares = dict.fromkeys(alpha_etfs)
        for etf in alpha_etfs:
            temp_etf_starting_price = etf_data_org[etf].loc[start_date:, 'Adj Close'].values[0]
            temp_etf_share = round(each_portion_money / temp_etf_starting_price, 2)
            alpha_etfs_shares[etf] = temp_etf_share
        #
        # TODO 3 create portfolio money by every interation Rebalance Frequency
        begin_iteration = start_date
        end_iteration = start_date + pd.DateOffset(months=self.rebalance_freq)

        spy_values = etf_data_org['SPY'].loc[begin_iteration:end_iteration, 'Adj Close'] * initial_spy_share

        alpha_etf_values = pd.DataFrame(columns=alpha_etfs_shares.keys())

        for dict_etf, dict_share in alpha_etfs_shares.items():
            alpha_etf_values[dict_etf] = etf_data_org[dict_etf].loc[begin_iteration:end_iteration,
                                         'Adj Close'] * dict_share

        portfolio_df.loc[begin_iteration:end_iteration, 'Portfolio_Value'] = spy_values + alpha_etf_values.sum(1)

        portfolio_info = pd.DataFrame(columns=['start', 'end', 'spy_share', 'alpha_etf_info'], index=range(1, 100))

        batch = 1

        portfolio_info.loc[batch, 'start'] = begin_iteration
        portfolio_info.loc[batch, 'end'] = end_iteration
        portfolio_info.loc[batch, 'spy_share'] = initial_spy_share
        portfolio_info.loc[batch, 'alpha_etf_info'] = alpha_etfs_shares.items()


        last_iteration_end_date = alpha_etf_values.index[-1]

        last_iteration_end_date_list = [last_iteration_end_date]


        while end_iteration < end_date:
            latest_portfolio_value = portfolio_df.loc[last_iteration_end_date].values[0]

            growth_performance_calculate = etf_price.loc[begin_iteration:end_iteration, :]
            growth_performance_calculate = growth_performance_calculate.iloc[-1, :] / growth_performance_calculate.iloc[
                                                                                      0, :] - 1
            growth_performance_calculate.drop('SPY_trans_price', inplace=True)
            growth_performance_calculate = growth_performance_calculate.nlargest(3)

            alpha_etfs = growth_performance_calculate.index.tolist()
            alpha_etfs = [x.split('_')[0] for x in alpha_etfs]
            ## for each alpha ETFs
            each_portion_money = latest_portfolio_value * (1 - spy_weight) / len(alpha_etfs)
            alpha_etfs_shares = dict.fromkeys(alpha_etfs)


            batch += 1
            begin_iteration += pd.DateOffset(months=self.rebalance_freq, day=2)
            end_iteration += pd.DateOffset(months=self.rebalance_freq)

            for etf in alpha_etfs:
                temp_etf_starting_price = etf_data_org[etf].loc[begin_iteration:, 'Adj Close'].values[0]
                temp_etf_share = round(each_portion_money / temp_etf_starting_price, 2)
                alpha_etfs_shares[etf] = temp_etf_share

            #             print('\n')
            #             print(batch)
            #             print(begin_iteration)
            #             print(end_iteration)

            spy_starting_price = etf_data_org['SPY'].loc[begin_iteration:, 'Adj Close'].values[0]
            spy_share = round(latest_portfolio_value * spy_weight / spy_starting_price, 2)
            spy_values = etf_data_org['SPY'].loc[begin_iteration:end_iteration, 'Adj Close'] * spy_share

            alpha_etf_values = pd.DataFrame(columns=alpha_etfs_shares.keys())

            for dict_etf, dict_share in alpha_etfs_shares.items():
                alpha_etf_values[dict_etf] = etf_data_org[dict_etf].loc[begin_iteration:end_iteration,
                                             'Adj Close'] * dict_share

            portfolio_df.loc[begin_iteration:end_iteration, 'Portfolio_Value'] = spy_values + alpha_etf_values.sum(1)

            last_iteration_end_date = alpha_etf_values.index[-1]
            last_iteration_end_date_list.append(last_iteration_end_date)
            portfolio_info.loc[batch, 'start'] = begin_iteration
            portfolio_info.loc[batch, 'end'] = end_iteration
            portfolio_info.loc[batch, 'spy_share'] = spy_share
            portfolio_info.loc[batch, 'alpha_etf_info'] = alpha_etfs_shares.items()

        portfolio_info.dropna(axis='index', inplace=True)

        return portfolio_info, portfolio_df ,last_iteration_end_date_list


test=portfolio_sumulator()

portfolio_info, portfolio_df,last_iteration_end_date_list = test.alpha_portfolio()




portfolio_info_sourced_priced = pd.DataFrame(columns=etf_data_org.keys(),index = last_iteration_end_date_list )

for etf in etf_data_org.keys():
    price_data = etf_data_org[etf]
    portfolio_info_sourced_priced.loc[:,etf] = price_data.loc[last_iteration_end_date_list,'Adj Close']



# extend pandas functionality with metrics, etc.
qs.extend_pandas()

# fetch the daily returns for a stock
stock = qs.utils.download_returns('META')

# show sharpe ratio
qs.stats.sharpe(stock)

portfolio_df = portfolio_df.pct_change(1)

qs.reports.html(portfolio_df, "QQQ",output=True, download_filename='compare_with_qqq.html')
qs.reports.basic(portfolio_df, "SPY")



'''
they are the same, daily return. 
stock = qs.utils.download_returns('META')
meta_price = yf.download('META')
meta_price['Adj Close'].pct_change(1)
'''

# 2005-12-01
date = '20070301'
total= portfolio_df.loc[date].values[0]

date = '20070302'

spy = etf_data_org['SPY'].loc[date,'Adj Close']
spy_share = total*0.6/spy
print(spy_share)



etf1= 'VAW'
etf2= 'VOX'
etf3 = 'VPU'

etf1_price= etf_data_org[etf1].loc[date,'Adj Close']
etf2_price= etf_data_org[etf2].loc[date,'Adj Close']
etf3_price= etf_data_org[etf3].loc[date,'Adj Close']

etf1_share = total*0.4/3/etf1_price
etf2_share = total*0.4/3/etf2_price
etf3_share = total*0.4/3/etf3_price



for etf in etf_data_org.keys():
    price_data = etf_data_org[etf]
    test = price_data.loc['20051202','Adj Close']
    print(etf+'__'+str(test))










