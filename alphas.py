#importing world quant libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
import scipy.stats as stats
import math
import time
import datetime
import os
import sys
import pickle
import warnings
warnings.filterwarnings('ignore')

# importing custom libraries
from utils import *
from data import *
from alphas import *
from backtest import *

# importing sklearn libraries
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Ridge
from sklearn.linear_model import Lasso
from sklearn.linear_model import ElasticNet

# importing keras libraries
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers import Dropout
from keras.layers import Activation
from keras.layers import Flatten
from keras.layers import TimeDistributed
from keras.layers import RepeatVector
from keras.layers import Bidirectional

# importing keras callbacks
from keras.callbacks import EarlyStopping
from keras.callbacks import ModelCheckpoint
from keras.callbacks import ReduceLROnPlateau

# Path: backtest.py

# 52 week high
def alpha_001(df, timeperiod=52):
    """
    Alpha_001: (close - max(close, timeperiod)) / max(close, timeperiod) * 100
    """
    df['alpha_001'] = (df['close'] - df['close'].rolling(timeperiod).max()) / df['close'].rolling(timeperiod).max() * 100
    return df

# 52 week low
def alpha_002(df, timeperiod=52):
    """
    Alpha_002: (min(close, timeperiod) - close) / min(close, timeperiod) * 100
    """
    df['alpha_002'] = (df['close'].rolling(timeperiod).min() - df['close']) / df['close'].rolling(timeperiod).min() * 100
    return df

# 52 week high indicator
def alpha_003(df, timeperiod=52):
    """
    Alpha_003: (close == max(close, timeperiod)) ? 1 : 0
    """
    df['alpha_003'] = np.where(df['close'] == df['close'].rolling(timeperiod).max(), 1, 0)
    return df

# 52 week low indicator
def alpha_004(df, timeperiod=52):
    """
    Alpha_004: (close == min(close, timeperiod)) ? 1 : 0
    """
    df['alpha_004'] = np.where(df['close'] == df['close'].rolling(timeperiod).min(), 1, 0)
    return df

# 52 week high - low
def alpha_005(df, timeperiod=52):
    """
    Alpha_005: (max(close, timeperiod) - min(close, timeperiod)) / min(close, timeperiod) * 100
    """
    df['alpha_005'] = (df['close'].rolling(timeperiod).max() - df['close'].rolling(timeperiod).min()) / df['close'].rolling(timeperiod).min() * 100
    return df

# 52 week high - low indicator
def alpha_006(df, timeperiod=52):
    """
    Alpha_006: (close == max(close, timeperiod)) ? 1 : ((close == min(close, timeperiod)) ? -1 : 0)
    """
    df['alpha_006'] = np.where(df['close'] == df['close'].rolling(timeperiod).max(), 1, np.where(df['close'] == df['close'].rolling(timeperiod).min(), -1, 0))
    return df


# 3 day moving average of volume
def alpha_007(df, timeperiod=3):
    """
    Alpha_007: SMA(volume, timeperiod, 1)
    """
    df['alpha_007'] = df['volume'].rolling(timeperiod).mean()
    return df

# 10 day moving average of volume
def alpha_008(df, timeperiod=10):
    """
    Alpha_008: SMA(volume, timeperiod, 1)
    """
    df['alpha_008'] = df['volume'].rolling(timeperiod).mean()
    return df

# 3 day moving average of close price
def alpha_009(df, timeperiod=3):
    """
    Alpha_009: SMA(close, timeperiod, 1)
    """
    df['alpha_009'] = df['close'].rolling(timeperiod).mean()
    return df

# 10 day moving average of close price
def alpha_010(df, timeperiod=10):
    """
    Alpha_010: SMA(close, timeperiod, 1)
    """
    df['alpha_010'] = df['close'].rolling(timeperiod).mean()
    return df

# 10 day moving average of close price / 3 day moving average of close price
def alpha_011(df, timeperiod1=10, timeperiod2=3):
    """
    Alpha_011: SMA(close, timeperiod1, 1) / SMA(close, timeperiod2, 1)
    """
    df['alpha_011'] = df['close'].rolling(timeperiod1).mean() / df['close'].rolling(timeperiod2).mean()
    return df

# 10 day moving average of volume / 3 day moving average of volume
def alpha_012(df, timeperiod1=10, timeperiod2=3):
    """
    Alpha_012: SMA(volume, timeperiod1, 1) / SMA(volume, timeperiod2, 1)
    """
    df['alpha_012'] = df['volume'].rolling(timeperiod1).mean() / df['volume'].rolling(timeperiod2).mean()
    return df

# (close - vwap) / close
def alpha_013(df):
    """
    Alpha_013: (close - vwap) / close
    """
    df['alpha_013'] = (df['close'] - df['vwap']) / df['close']
    return df



# (close - open) / open
def alpha_014(df):
    """
    Alpha_014: (close - open) / open
    """
    df['alpha_014'] = (df['close'] - df['open']) / df['open']
    return df

# (close - low) / (high - low)
def alpha_015(df):
    """
    Alpha_015: (close - low) / (high - low)
    """
    df['alpha_015'] = (df['close'] - df['low']) / (df['high'] - df['low'])
    return df

# (close - vwap) / (vwap - open)
def alpha_016(df):
    """
    Alpha_016: (close - vwap) / (vwap - open)
    """
    df['alpha_016'] = (df['close'] - df['vwap']) / (df['vwap'] - df['open'])
    return df 