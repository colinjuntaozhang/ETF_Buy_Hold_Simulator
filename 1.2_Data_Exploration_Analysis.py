import pandas as pd
import numpy as np
import pickle
import matplotlib.pyplot as plt
import seaborn as sns

with open('data/etf_data.pickle','rb') as f:
    etf_data_org = pickle.load(f)


def add_transform_data_daily_return(x,key):
    output = x[['Adj Close','Volume']].copy()
    output[f'{key}_trans_price'] = output['Adj Close']/output['Adj Close'][0]
    output.rename({"Adj Close":f"{key}_adj_close"}, axis='columns', inplace=True)
    output.rename({"Volume":f"{key}_Volume"}, axis='columns', inplace=True)
    return output

etf_data = dict.fromkeys(etf_data_org)


for key in etf_data.keys():
    etf_data[key] = add_transform_data_daily_return(etf_data_org[key],key)


combine_all_keys = list(etf_data.keys())

combine_all_keys = [x+'_trans_price' for x in combine_all_keys]

all_transformed_price = pd.DataFrame(index = etf_data['SPY'].index, columns=combine_all_keys)

for key in etf_data.keys():
    all_transformed_price[f'{key}_trans_price'] = etf_data[key][f'{key}_trans_price']


all_transformed_price.plot(grid=True)
all_transformed_price.loc['2005':'2007'].plot(grid=True)

#
# plt.figure(figsize=(25, 8))
# plt.title('daily return')
# plt.plot(spy_data.index[-20:], spy_data['adj_change_daily'][-20:], 'r-', label='adj close')
# plt.plot(spy_data.index[-20:], spy_data['tran_change_daily'][-20:], 'g-',label='transform price')
# plt.legend(loc='upper left')
# plt.show()


