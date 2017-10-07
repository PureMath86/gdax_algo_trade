import gdax
# import time
# from datetime import datetime
import pandas as pd
# import sys


class CryptoTrade:
    def __init__(self, name):

        self.name = name
        self.login = pd.read_csv(r'C:\dev\gdax\login.txt')
        self.auth_client = gdax.AuthenticatedClient(
            self.login["BLANK LINE"][1],
            self.login["BLANK LINE"][2],
            self.login["BLANK LINE"][0])

        self.public_client = gdax.PublicClient()
        self.acc_db = self.get_all_acc()

    def get_all_acc(self):
        acc_list = self.auth_client.get_accounts()

        acc_db = {}
        for entry in acc_list:
            name = entry.pop("currency")
            acc_db[name] = entry

        return acc_db

    def get_acc_balance(self, currency):
        acc_id = self.acc_db[currency]["id"]
        return self.auth_client.get_account(acc_id)["balance"]

    # def get_ask(self,product):
    #     return float(self.public_client.get_product_ticker(product)["ask"])

    # def get_bid(self,product):
    #     return float(self.public_client.get_product_ticker(product)["bid"])

    def get_ask_bid(self, product):
        ticker = self.public_client.get_product_ticker(product)
        ask = float(ticker["ask"])
        bid = float(ticker["bid"])
        return {"ask": ask, "bid": bid}

    # def get_target_ask(self, product):
    #
    #     bsg = 0.25  # buy/sell gain
    #     max_buy_price = self.get_bid(product) * (1 - (bsg / 100))
    #     min_sell_price = self.get_ask(product) * (1 + (bsg / 100))
    #
    #     return round(max(max_buy_price, min_sell_price), 2)

    # def get_target_bid(self,product):
    #
    #     bsg = 0.25  # buy/sell gain
    #     max_buy_price = self.get_bid(product) * (1 - (bsg / 100))
    #     min_sell_price = self.get_ask(product) * (1 + (bsg / 100))
    #
    #     return round(min(max_buy_price, min_sell_price), 2)

    def get_targets(self, product):

        bsg = 0.25  # buy/sell gain
        # max_buy_price = self.get_bid(product) * (1 - (bsg / 100))
        # min_sell_price = self.get_ask(product) * (1 + (bsg / 100))
        g_s_b = self.get_ask_bid(product)

        max_buy_price = g_s_b["bid"] * (1 - (bsg / 100))
        min_sell_price = g_s_b["ask"] * (1 + (bsg / 100))
        target_ask = round(max(max_buy_price, min_sell_price), 2)
        target_bid = round(min(max_buy_price, min_sell_price), 2)
        return {"target_ask": target_ask, "target_bid": target_bid}

    def trade_market_maker(self, product):

        trade_size = 0.05

        # a = float(self.get_ask(product))
        # b = float(self.get_bid(product))
        ask_bid = self.get_ask_bid(product)
        a = float(ask_bid["ask"])
        b = float(ask_bid["bid"])
        # t_a = float(self.get_target_ask(product))
        # t_b = float(self.get_target_bid(product))
        targets = self.get_targets(product)
        t_a = float(targets["target_ask"])
        t_b = float(targets["target_bid"])

        fiat_acc = float(self.get_acc_balance(product.split(sep="-")[1]))  # EUR
        cryp_acc = float(self.get_acc_balance(product.split(sep="-")[0]))  # ETH

        if fiat_acc > t_a * trade_size:
            print("Buy Crypto Possible")
            print("Ask: " + str(a) + " and Target Ask " + str(t_a))
            print("Bid: " + str(b) + " and Target Bid " + str(t_b))
            # self.auth_client.buy(price=t_b, size=trade_size, product_id=product)
        else:
            print("Insufficient Balance")
            # self.auth_client.sell(price=t_a, size=trade_size, product_id=product)

        if cryp_acc > trade_size:
            print("Sell Crypto Possible")
            print("Ask: " + str(a) + " and Target Ask " + str(t_a))
            print("Bid: " + str(b) + " and Target Bid " + str(t_b))
        else:
            print("Insufficient Balance")
            # self.auth_client.sell(price=t_a, size=trade_size, product_id=product)


# trade = CryptoTrade("trade")
# trade.trade_market_maker("ETH-EUR")

