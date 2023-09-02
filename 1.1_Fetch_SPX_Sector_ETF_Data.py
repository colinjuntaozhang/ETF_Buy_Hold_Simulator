import yfinance as yf
import pickle


# use SPY, instead of 'VOO', the history of VOO is too short
etf_tickers = ['SPY','VOX','VCR','VDC','VDE','VFH','VHT','VIS','VGT','VAW','VNQ','VPU']

etf_data = {}

## download the data from yahoo finance, it has Open, High, Low, Close, Adj Close, Volume
## cut the data from the beginning of 2005 to the end of 2021.
## because all the Vanguard sector etf started from feb or oct 2004.
for ticker in etf_tickers:
    temp_data = yf.download(ticker)
    etf_data[ticker] = temp_data['2005':'2021']

'''
save the data to pickle 
and load it from pickle 
'''

#
# with open('data/etf_data.pickle', 'wb') as f:
#     pickle.dump(etf_data, f)
#
# with open('data/etf_data.pickle','rb') as f:
#     etf_data = pickle.load(f)







