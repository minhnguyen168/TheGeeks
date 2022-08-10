#!/usr/bin/env python
# coding: utf-8
# from flask import Flask, render_template
#
# app = Flask(__name__)
#
# @app.route('/')


import yfinance as yf
from datetime import date
from dateutil.relativedelta import relativedelta



# get market details
def get_market_details(markets):
    tickers = []
    for market in markets:
        tickers.append(yf.Ticker(market))
    return tickers


# display market details
def display_market_details(markets, tickers):
    # variable to store market to display more detailed information in next page
    button_value = 0

    # display each market info in a box
    for index in range(len(markets)):
        print('Market: ', markets[index], '\n')
        print('Current Price: ', tickers[index].info['currentPrice'], '\n')
        print('Earnings Growth: ', tickers[index].info['earningsGrowth'], '\n')
        print('Current Ratio: ', tickers[index].info['currentRatio'], '\n')
        print('Return on Assets: ', tickers[index].info['returnOnAssets'], '\n')

        button_value = markets[index]  # to be stored in button id


# when the user clicks on a particular market, it will display more details
def get_more_details(market_name):
    ticker = yf.Ticker(market_name)

    print('Market: ', market_name, '\n')
    print(ticker.info['longBusinessSummary'], '\n')
    print('Current Price: ', ticker.info['currentPrice'], '\n')
    print('Earnings Growth: ', ticker.info['earningsGrowth'], '\n')
    print('Current Ratio: ', ticker.info['currentRatio'], '\n')
    print('Return on Assets: ', ticker.info['returnOnAssets'], '\n')
    print('Target Mean Price: ', ticker.info['targetMeanPrice'], '\n')
    print('Debt to Equity: ', ticker.info['debtToEquity'], '\n')
    print('Return on Equity: ', ticker.info['returnOnEquity'], '\n')
    print('Target High Price: ', ticker.info['targetHighPrice'], '\n')
    print('Total Cash: ', ticker.info['totalCash'], '\n')
    print('Total Debt: ', ticker.info['totalDebt'], '\n')
    print('Total Revenue: ', ticker.info['totalRevenue'], '\n')

    # button to purchase stock here


# holding periods of 1 week, 1 month, 1 year and 5 years
def get_holding_periods(end):
    wk_1 = end - relativedelta(weeks=+1)
    mth_1 = end - relativedelta(months=+6)
    yr_1 = end - relativedelta(years=+1)
    yr_5 = end - relativedelta(years=+5)

    return [wk_1, mth_1, yr_1, yr_5]


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


# think it's better to display in table instead of chart because interval is not consistent and too big


# main
def main():
    # list of sample markets
    markets = ['NVDA', 'BBBY', 'GME', 'NVAX', 'MU', 'INTC', 'LMND', 'NCLH', 'VRNA', 'AMAT', 'U', 'NLSN', 'VTNR', 'PUBM',
               'OXY', 'SWAV', 'APP', 'GDRX', 'BIRD', 'RETO', 'LRCX', 'TTOO', 'LAZR', 'UPST', 'TUEM', 'TREX', 'ENDP',
               'IS', 'CARG', 'TTWO', 'DVN', 'MRSN'
               ]

    tickers = get_market_details(markets)

    display_market_details(markets, tickers)

    button_id = 'NVDA'  # simulate

    get_more_details(button_id)

    end = date.today()

    periods = get_holding_periods(end)

    hist_df = get_hist_ret(button_id, periods, end)

    portfolio_returns = cal_port_ret(len(periods), hist_df)


if __name__ == "__main__":
    main()

# def index():
#     return render_template("trade.html")
#
# if "__name__" == "__main__":
#     app.run(debug=True)


