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
    day_before_ytd = end - timedelta(days=2)

    return day_before_ytd


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

def cal_1d_diff(market_name, start, end):
    hist_df = yf.download(market_name, start=start, end=end)
    adj_close = hist_df['Adj Close']
    return adj_close.pct_change()[-1]  # get percentage change between the day before ytd and ytd

# main

# list of sample markets
# markets = ['NVDA', 'BBBY', 'GME', 'NVAX', 'MU', 'INTC', 'LMND', 'NCLH', 'VRNA', 'AMAT', 'U', 'NLSN', 'VTNR', 'PUBM',
#            'OXY', 'SWAV', 'APP', 'GDRX', 'BIRD', 'RETO', 'LRCX', 'TTOO', 'LAZR', 'UPST', 'TUEM', 'TREX', 'ENDP',
#            'IS', 'CARG', 'TTWO', 'DVN', 'MRSN'
#            ]

# to add in routes.py
# @app.route('/client/returns_test', methods=['GET', 'POST'])
# def get_1d_diff():
#     market_name = 'NVDA'
#     today = trade.get_today()
#     start = trade.get_one_day_period(today)
#     print(trade.cal_1d_diff(market_name, start, today)) # should have two records
#     return render_template()


