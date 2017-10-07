import gdax
import time
# import datetime
# import csv
import sys
import pandas as pd
# import json

public_client = gdax.PublicClient()

def getHFTdata(public_client):
    # get latest trades
    eth_eur_trades = public_client.get_product_trades(product_id='ETH-EUR')
    trades_df = pd.DataFrame(eth_eur_trades)
    trades_df["price"] = trades_df["price"].astype(float)
    trades_df["size"] = trades_df["size"].astype(float)

    # order book function call
    ord_book = public_client.get_product_order_book('ETH-EUR', level = 2)
    labels = ["price", "size", "num-orders"]

    # convert to df
    asks_df = pd.DataFrame.from_records(ord_book["asks"], columns=labels)
    bids_df = pd.DataFrame.from_records(ord_book["bids"], columns=labels)

    # convert to float and add cumsum
    asks_df = asks_df.astype(float)
    asks_df["cum-val"] = asks_df["size"].cumsum()
    bids_df = bids_df.astype(float)
    bids_df["cum-val"] = bids_df["size"].cumsum()

    fileName = "C:\dev\gdax_data" + "\gdax_book_"+ str(int(time.time()))+".xlsx"

    writer = pd.ExcelWriter(fileName)
    asks_df.to_excel(writer,'asks_df')
    bids_df.to_excel(writer,'bids_df')

    trades_df.to_excel(writer,'trades_df')

    writer.save()

    time.sleep(59)



i = 0
while 0 < 1:
    try:
        getHFTdata(public_client)
        # print(str(i), end="\r")
        # i += 1
    except:
        e = sys.exc_info()[0]
        print(e)
        time.sleep(60)
