# coding: utf-8


import gdax
import time
from datetime import datetime
import pandas as pd
import sys

public_client = gdax.PublicClient()

# Get the order book at the default level.
# public_client.get_product_order_book('BTC-GBP')
# Get the order book at a specific level.
# public_client.get_product_order_book('BTC-GBP', level=1)

# Get the product ticker for a specific product.
public_client.get_product_ticker(product_id='BTC-GBP')

# Get the product trades for a specific product.
# public_client.get_product_trades(product_id='BTC-GBP')


public_client.get_product_historic_rates('BTC-GBP')
# To include other parameters, see function docstring:
public_client.get_product_historic_rates('BTC-GBP', granularity=3000)

# login text file... see readme

if sys.platform == 'linux':
    print("linux")
    login = pd.read_csv('/home/richard/dev/login.txt')

else:
    print("windows")
    login = pd.read_csv(r'C:\dev\gdax\login.txt')

auth_client = gdax.AuthenticatedClient(login["BLANK LINE"][1], login["BLANK LINE"][2], login["BLANK LINE"][0])


def placeBuyOrSellOrder(algoFreq):
    tradingActive = False
    print("Trading Algo Active: " + str(tradingActive))

    running = input

    # define fiat account
    gbp_acc = auth_client.get_account(login["BLANK LINE"][3])

    # define cyrpto account
    btc_acc = auth_client.get_account(login["BLANK LINE"][4])

    # get market price
    latest_price = float(public_client.get_product_ticker(product_id='BTC-GBP')["price"])

    # get market prices
    price_ask = float(public_client.get_product_ticker(product_id='BTC-GBP')["ask"])
    price_bid = float(public_client.get_product_ticker(product_id='BTC-GBP')["bid"])
    mid_market = (price_ask + price_bid) * 0.5

    # amount of crypto to trade
    btc_trade_vol = 0.05

    # margin as factor before purchase for crypto reserve
    btc_trade_margin = 1.0

    # create buy price
    max_buy_price = price_bid * 0.9825
    target_buy = str(round(min(max_buy_price, price_bid * 0.9875), 2))

    # create sell price
    min_sell_price = price_ask * 1.0125
    target_sell = str(round(max(min_sell_price, price_bid * 1.0125), 2))

    # BUY if funds availble
    if float(gbp_acc["available"]) > latest_price * btc_trade_vol * btc_trade_margin:
        print('BUY order £' + target_buy + " : Mid Market £" + str(mid_market) + " : " + str(datetime.now()))

        if tradingActive == True:
            auth_client.buy(price=target_buy,size=btc_trade_vol,product_id='BTC-GBP')
        else:
            print(str(target_buy))

    # SELL if BTC availble
    else:
        if float(btc_acc["available"]) > btc_trade_vol:

            print('SELL order ' + target_sell + " : Bid Market £" + str(price_bid) + " : " + str(datetime.now()))

            if tradingActive == True:

                auth_client.sell(price=target_sell,
                         size=str(btc_trade_vol),  # BTC
                         product_id='BTC-GBP')
        else:
            print(str(target_sell))


    time.sleep(algoFreq)



algoFreq = 5  # seconds

while 1 < 2:
    placeBuyOrSellOrder(algoFreq)
    time.sleep(algoFreq)
