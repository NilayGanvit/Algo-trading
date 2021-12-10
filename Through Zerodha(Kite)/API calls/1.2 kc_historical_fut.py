
from kiteconnect import KiteConnect
import os
import datetime as dt
import pandas as pd

cwd = os.chdir("D:\\Udemy\\Zerodha KiteConnect API\\1_account_authorization")


access_token = open("access_token.txt",'r').read()
key_secret = open("api_key.txt",'r').read().split()
kite = KiteConnect(api_key=key_secret[0])
kite.set_access_token(access_token)



instrument_dump = kite.instruments("NFO")
instrument_df = pd.DataFrame(instrument_dump)
fut_df = instrument_df[instrument_df["segment"]=="NFO-FUT"]

def instrumentLookup(instrument_df,symbol):
    
    try:
        return instrument_df[instrument_df.tradingsymbol==symbol].instrument_token.values[0]
    except:
        return -1


def fetchOHLC(ticker,interval,duration):
    
    instrument = instrumentLookup(instrument_df,ticker)
    data = pd.DataFrame(kite.historical_data(instrument,dt.date.today()-dt.timedelta(duration), dt.date.today(),interval))
    data.set_index("date",inplace=True)
    return data

fetchOHLC("NIFTY20MAYFUT","5minute",4)
