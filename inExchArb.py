import gdax
import time
import datetime
import csv
import sys

public_client = gdax.PublicClient()

def currArb(public_client):
    # pull price data
    btc_eur = public_client.get_product_ticker(product_id='BTC-EUR')
    eth_eur = public_client.get_product_ticker(product_id='ETH-EUR')
    ltc_eur = public_client.get_product_ticker(product_id='LTC-EUR')
    eth_btc = public_client.get_product_ticker(product_id='ETH-BTC')
    ltc_btc = public_client.get_product_ticker(product_id='LTC-BTC')

    #split into actual rates
    eur2btc = 1/float(btc_eur["ask"])
    btc2eur = float(btc_eur["bid"])

    eur2eth = 1/float(eth_eur["ask"])
    eth2eur = float(eth_eur["bid"])

    eur2ltc = 1/float(ltc_eur["ask"])
    ltc2eur = float(ltc_eur["bid"])

    btc2eth = 1/float(eth_btc["ask"])
    eth2btc = float(eth_btc["bid"])

    btc2ltc = 1/float(ltc_btc["ask"])
    ltc2btc = float(ltc_btc["bid"])

    #### PATH 1A ####
    eur_btc_eth_eur = 1 * eur2btc * btc2eth * eth2eur

    #### PATH 1B ####
    eur_eth_btc_eur = 1 * eur2eth * eth2btc * btc2eur

    #### PATH 2A ####
    eur_btc_ltc_eur = 1 * eur2btc * btc2ltc * ltc2eur

    #### PATH 2B ####
    eur_ltc_btc_eur = 1 * eur2ltc * ltc2btc * btc2eur

    arb_paths = ["eur_btc_eth_eur", "eur_eth_btc_eur", "eur_btc_ltc_eur", "eur_ltc_btc_eur"]
    arb_values = [eur_btc_eth_eur,eur_eth_btc_eur,eur_btc_ltc_eur,eur_ltc_btc_eur]


    arb_dict = dict(zip(arb_paths, arb_values))
    arb_max = max(arb_dict, key=arb_dict.get)


    i = datetime.datetime.now()

    # write to local csv
    fields=[i.isoformat(),arb_max,str(max(arb_values)),str(eur2btc),str(btc2eur),str(eur2eth),str(eth2eur),str(eur2ltc),str(ltc2eur),str(btc2eth),str(eth2btc),str(btc2ltc),str(ltc2btc)]

    #with open(r'C:\dev\gdax.csv', 'a') as f:
    with open(r'C:\dev\gdax.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(fields)

    time.sleep(15)

i = 0
while 0 < 1:
    try:
        currArb(public_client)
        #print(str(i), end="\r")
    except:
        e = sys.exc_info()[0]
        print(e)
        time.sleep(60)


#### PATH 3A ####
#path_3a = 1 * eur2eth * eth2ltc * ltc2eur
# EUR>ETH
# ETH>LTC
# LTC>EUR

#### PATH 3B ####
#path_3b = 1 * eur2ltc * ltc2eth * eth2eur
# EUR>LTC
# LTC>ETH
# ETH>EUR

