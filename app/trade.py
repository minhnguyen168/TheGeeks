#!/usr/bin/env python
# coding: utf-8



import yfinance as yf
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta



# get market details
def get_market_details(markets):
    tickers = []

    for market in markets:
        tickers.append(yf.Ticker(market))
    return tickers

def get_today():
    return date.today()

# holding periods of 1 week, 1 month, 1 year and 5 years
def get_holding_periods(end):
    wk_1 = end - relativedelta(weeks=+1)
    mth_1 = end - relativedelta(months=+6)
    yr_1 = end - relativedelta(years=+1)
    yr_5 = end - relativedelta(years=+5)

    return [wk_1, mth_1, yr_1, yr_5]

def get_one_day_period(end):
    one_day_before = end - timedelta(days=1)
    day_before_ytd = end - timedelta(days=2)

    return [one_day_before, day_before_ytd]


# calculate asset returns for a current portfolio? e.g. assuming client selected NVDA stocks only (should we do this for assets they want to buy or their entire portfolio)
def get_hist_ret(market_name, periods, end):
    df = []
    for period in periods:
        df.append(yf.download(market_name, start=period, end=end))

    return df

# for each holding period, calculate the portfolio mean
def cal_port_ret(num_periods, hist_df):
    portfolio_means = []
    for index in range(num_periods):
        adj_close = hist_df[index]['Adj Close']
        returns = adj_close.pct_change()[1:]  # get percentage change between the days -> remove first entry because NA
        portfolio_means.append(returns.mean())

    return portfolio_means

def cal_1d_diff(hist_df):
    adj_close = hist_df['Adj Close']
    return adj_close.pct_change()[1]  # get percentage change between the days -> remove first entry because NA


# main

# list of sample markets
# markets = ['NVDA', 'BBBY', 'GME', 'NVAX', 'MU', 'INTC', 'LMND', 'NCLH', 'VRNA', 'AMAT', 'U', 'NLSN', 'VTNR', 'PUBM',
#            'OXY', 'SWAV', 'APP', 'GDRX', 'BIRD', 'RETO', 'LRCX', 'TTOO', 'LAZR', 'UPST', 'TUEM', 'TREX', 'ENDP',
#            'IS', 'CARG', 'TTWO', 'DVN', 'MRSN'
#            ]

# Branda
# today = trade.get_today()
# periods = trade.get_holding_periods(today)
# hist_df = trade.get_hist_ret(market_name, periods, end) # should have two records
# pct_diff = trade.cal_1d_diff(hist_df)

