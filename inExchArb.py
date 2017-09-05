import gdax

public_client = gdax.PublicClient()

btc_eur = public_client.get_product_ticker(product_id='BTC-EUR')
eth_eur = public_client.get_product_ticker(product_id='ETH-EUR')
ltc_eur = public_client.get_product_ticker(product_id='LTC-EUR')

eth_btc = public_client.get_product_ticker(product_id='ETH-BTC')
ltc_btc = public_client.get_product_ticker(product_id='LTC-BTC')

# < ASK (what someone is willing to sell)
# > BID (what someone is willing to pay)

# simplfy
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
path_1a = 1 * eur2btc * btc2eth * eth2eur

#### PATH 1B ####
path_1b = 1 * eur2eth * eth2btc * btc2eur

#### PATH 2A ####
path_2a = 1 * eur2btc * btc2ltc * ltc2eur

#### PATH 2B ####
path_2b = 1 * eur2ltc * ltc2btc * btc2eur


print(str((max(path_1a,path_1b,path_2a,path_2b)-1)*100))





















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

