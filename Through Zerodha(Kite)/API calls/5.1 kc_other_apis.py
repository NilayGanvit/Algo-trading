
from kiteconnect import KiteConnect
import os


cwd = os.chdir("D:\\Udemy\\Zerodha KiteConnect API\\1_account_authorization")


access_token = open("access_token.txt",'r').read()
key_secret = open("api_key.txt",'r').read().split()
kite = KiteConnect(api_key=key_secret[0])
kite.set_access_token(access_token)



quote = kite.quote("NSE:INFY")


ltp = kite.ltp("NSE:INFY")


orders = kite.orders()


positions = kite.positions()


holdings = kite.holdings()
