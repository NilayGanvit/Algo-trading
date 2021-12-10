
from kiteconnect import KiteConnect
import pandas as pd

api_key = "Your API Key"
api_secret = "Your API Secret"
kite = KiteConnect(api_key=api_key)
print(kite.login_url()) 


request_token = "Your Request Token" 
data = kite.generate_session(request_token, api_secret=api_secret)


kite.set_access_token(data["access_token"])



instrument_dump = kite.instruments("NSE")
instrument_df = pd.DataFrame(instrument_dump)
instrument_df.to_csv("NSE_Instruments.csv",index=False)