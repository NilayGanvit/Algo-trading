
from kiteconnect import KiteConnect
import pandas as pd
import datetime as dt
import os
import numpy as np
from stocktrends import Renko

cwd = os.chdir("D:\\Udemy\\Zerodha KiteConnect API\\1_account_authorization")


access_token = open("access_token.txt",'r').read()
key_secret = open("api_key.txt",'r').read().split()
kite = KiteConnect(api_key=key_secret[0])
kite.set_access_token(access_token)


instrument_dump = kite.instruments("NSE")
instrument_df = pd.DataFrame(instrument_dump)

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

def atr(DF,n):
    
    df = DF.copy()
    df['H-L']=abs(df['high']-df['low'])
    df['H-PC']=abs(df['high']-df['close'].shift(1))
    df['L-PC']=abs(df['low']-df['close'].shift(1))
    df['TR']=df[['H-L','H-PC','L-PC']].max(axis=1,skipna=False)
    df['ATR'] = df['TR'].ewm(com=n,min_periods=n).mean()
    
    return df['ATR']

def renko_DF(DF):
    
    df = DF.copy()
    df.reset_index(inplace=True)
    df2 = Renko(df)
    df2.brick_size = 10
    renko_df = df2.get_ohlc_data()
    return renko_df

ohlc = fetchOHLC("HDFC","5minute",5)
renko = renko_DF(ohlc)