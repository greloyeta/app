
import streamlit as st
import pandas as pd
import math
import numpy as np
import pandas_datareader as web
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM
import matplotlib.pyplot as plt

st.markdown("""
#Stock Predictor
This website can predict the value of a stock price in the in the future
""")

st.write("""Disclaimer: Any investing is done at the investors expense, we are not responsible for any actions taken.
""")

try:
    ticker = st.text_input("Enter Ticker symbol below", "GOOGL")
    df = web.DataReader(ticker, data_source='yahoo', start='2012-01-01', end='2019-12-17')

except:
    ticker = 'GOOGL'
    df = web.DataReader(ticker, data_source='yahoo', start='2012-01-01', end='2019-12-17')

#visualization
st.line_chart(df['Close'])
st.caption(ticker+' stock price.')


valid, train, predictions = sp.make_model(df)

valid['Predictions'] = predictions

"""
Actual Price vs Predicted
"""
st.line_chart(valid)
