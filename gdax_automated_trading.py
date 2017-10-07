import gdax
# import time
# from datetime import datetime
import pandas as pd


# import sys


class CryptoTrade:
    # datetime = __import__("datetime")
    # threading = __import__("threading")

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
        g_s_b = self.get_ask_bid(product)

        max_buy_price = g_s_b["bid"] * (1 - (bsg / 100))
        min_sell_price = g_s_b["ask"] * (1 + (bsg / 100))

        target_ask = round(max(max_buy_price, min_sell_price), 2)
        target_bid = round(min(max_buy_price, min_sell_price), 2)
        return {"target_ask": target_ask, "target_bid": target_bid}

    def trade_market_maker(self, product):

        # put bids in below latest ask -  and asks in above latest bid

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

        fiat_acc = float(self.get_acc_balance(product.split(sep="-")[1]))  # e.g. EUR
        cryp_acc = float(self.get_acc_balance(product.split(sep="-")[0]))  # e.g. ETH

        # 25 of fiat currency / target bid of one unit
        # GDAX order constraint
        trade_size = max(round((10 / t_b), 6), 0.01)

        # messages
        print("Ask: " + str(a) + " and Target Ask " + str(t_a))
        print("Bid: " + str(b) + " and Target Bid " + str(t_b))

        if fiat_acc > t_a * trade_size:
            print("Buy Crypto Possible")
            print("Buying at " + str(t_b))
            # self.auth_client.buy(price=str(t_b), size=str(trade_size), product_id=product)
            self.auth_client.buy(price=str(t_b), size=str(trade_size), product_id=product,
                                 time_in_force="GTT", cancel_after="min")

        else:
            print("Insufficient " + product.split(sep="-")[1] + " fund to buy.")

        if cryp_acc > trade_size:
            print("Sell Crypto Possible")
            print("Selling at " + str(t_a))
            # self.auth_client.sell(price=str(t_a), size=str(trade_size), product_id=product)
            self.auth_client.sell(price=str(t_a), size=str(trade_size), product_id=product,
                                  time_in_force="GTT", cancel_after="min")

        else:
            print("Insufficient " + product.split(sep="-")[0] + " to sell.")

    def run_trade(self, product):
        import time

        while True:
            time.sleep(25)
            self.trade_market_maker(product)


trade = CryptoTrade("trade")

trade.run_trade("BTC-EUR")

# EOF
