import pandas as pd

def investment_simulation(ticker,start_date,end_date,invest_rule,invest_amount,save):
    stock_data = pd.read_csv(f'./data/{ticker}.csv')

    stock_data['Date'] = pd.to_datetime(stock_data['Date'])
    stock_data['DayName'] = stock_data['Date'].dt.day_name()
    stock_data['Year'] = stock_data['Date'].dt.year
    stock_data['Month'] = stock_data['Date'].dt.month
    stock_data['Day'] = stock_data['Date'].dt.day
    stock_data.set_index('Date',inplace=True)


    Rule_day = invest_rule.split('_')[0]
    Rule_week = invest_rule.split('_')[1]

    selected_data = stock_data.loc[start_date:end_date].copy()
    selected_data = selected_data[selected_data['DayName'] == Rule_day]

    if Rule_week != 'Week':
        selected_data = selected_data.iloc[::2]

    selected_data.loc[:,'InvestAmount'] = invest_amount
    selected_data.loc[:,'BuyingShares'] = selected_data['InvestAmount']/selected_data['Adj Close']

    summary_data_keys = ['Ticker','Start','End', 'Rule','TotalTimes','TotalInvest','TotalShares',
                                         'AvgCost','StartPrice','ClosePrice','EndValue','Profit','ProfitPct']

    summary_data_values = [ticker,start_date,end_date,invest_rule,len(selected_data),selected_data['InvestAmount'].sum(),
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
        output_name = "./output/"+ticker+"_"+start_date+"_"+end_date+invest_rule+'_'+str(invest_amount)+'_'+'.xlsx'

        with pd.ExcelWriter(output_name) as writer:
            selected_data.to_excel(writer, sheet_name='selected_data')
            summary_data.to_excel(writer, sheet_name='summary')

    return [selected_data, summary_data]


ticker = 'tqqq'
start_date = '2020-01-01'
end_date = '2021-12-31'
invest_rule = 'Wednesday_Biweek'  # 'Monday_Week' 'Monday_Biweek'
invest_amount = 100
save = False

results = investment_simulation(ticker,start_date,end_date,invest_rule,invest_amount, save)
print(results[1])



