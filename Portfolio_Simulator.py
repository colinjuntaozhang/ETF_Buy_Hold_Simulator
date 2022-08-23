#=================================================================================#
# This file is to build a portfolio contractor                                    #
# 1. unlimited stock tickers                                                      #
# 2. different weight or different fixed amount for each ticker                   #
# 3. can combine different period portfolio together                              #
#    like from 2010-2015 70/30, combine 2015-2020 80/20                           #
#    and get total final financial performance                                    #
# 4. can be more intelligent by setting some rules                                #
# 5. dynamically change amount from certain range                                 #
# 6. dynamically change allocation based on certain rules like 50-days average    #
#                                                                                 #
#                                                                                 #
#                                                                                 #
#=================================================================================#

import os
import pandas as pd
import numpy as np
import pandas_datareader.data as web
import datetime



def buy_stock(ticker, start, end, amount, invest_rule,save):

    stock_data = web.DataReader(ticker,'yahoo',start,end)

    stock_data['DayName'] = stock_data.index.day_name()
    stock_data['Year'] = stock_data.index.year
    stock_data['Month'] = stock_data.index.month
    stock_data['Day'] = stock_data.index.day

    Rule_day = invest_rule.split('_')[0]
    Rule_week = invest_rule.split('_')[1]

    selected_data = stock_data.loc[start:end].copy()
    selected_data = selected_data[selected_data['DayName'] == Rule_day]

    if Rule_week != 'Week':
        selected_data = selected_data.iloc[::2]

    selected_data.loc[:,'InvestAmount'] = amount
    selected_data.loc[:,'BuyingShares'] = selected_data['InvestAmount']/selected_data['Adj Close']

    summary_data_keys = ['Ticker','Start','End', 'Rule','TotalTimes','TotalInvest','TotalShares',
                                         'AvgCost','StartPrice','ClosePrice','EndValue','Profit','ProfitPct']

    summary_data_values = [ticker,start,end,invest_rule,len(selected_data),selected_data['InvestAmount'].sum(),
                           selected_data['BuyingShares'].sum(),
                           selected_data['InvestAmount'].sum()/selected_data['BuyingShares'].sum(),
                           selected_data['Adj Close'][0],
                           selected_data['Adj Close'][-1],
                           selected_data['Adj Close'][-1]*selected_data['BuyingShares'].sum(),
                           selected_data['Adj Close'][-1]*selected_data['BuyingShares'].sum() - selected_data['InvestAmount'].sum(),
                           (selected_data['Adj Close'][-1]*selected_data['BuyingShares'].sum())/(selected_data['InvestAmount'].sum())]

    summary_data = pd.DataFrame(list(zip(summary_data_keys,summary_data_values)), columns=['Item','Value'])
    summary_data.set_index('Item',inplace=True)

    if save:
        output_name = "./output/"+ticker+"_"+start+"_"+end+invest_rule+'_'+str(amount)+'_'+'.xlsx'

        with pd.ExcelWriter(output_name) as writer:
            selected_data.to_excel(writer, sheet_name='selected_data')
            summary_data.to_excel(writer, sheet_name='summary')

    return [selected_data, summary_data]


start = datetime.datetime(2021,1,1)
end = datetime.datetime(2022,6,10)
ticker = 'TSLA'
invest_rule = 'Wednesday_Biweek'
amount = 100
save = False

output = buy_stock(ticker, start, end, amount, invest_rule,save)
print(output[1])


# class Portfolio_Construction:

payload=pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
first_table = payload[0]
second_table = payload[1]

df = first_table



from transformers import pipeline

classifier = pipeline("sentiment-analysis")  # 情感分析
classifier("I've been waiting for a HuggingFace course my whole life.")






