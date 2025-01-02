


# https://www.ally.com/api/invest/documentation/trading/
# side = 1: buy, side = 2, sell
# typ = 1: market order, typ =2 : limit order
# TmInForce=0: day order, TmInForce=1: GTC (60days)
# ONLY IND have naked call options
import requests
import json
import pandas as pd
import numpy as np
from requests_oauthlib import OAuth1
import xml.etree.ElementTree as et
from func import 
 AccountNumber, Secret*
from func.order import Order
from func.orderfunc import  get_order_list
from func.option import Option
from func.quote import Quote
from func.orderfunc import get_order_list, cancel_order
from datetime import datetime, timezone, date, timedelta
from func.utility import closest_value
from func.stream import JSONStreamParser, stream_request
from requests import Request, Session

# trad, ind, roth
# 1.get option expiration date and strike price

auth = OAuth1(consumer_key, consumer_secret, oath_token, oath_token_secret)
ticker = 'BABA'
put_call = 'call'

# prepare URL:
stock_url = f"https://devapi-stream.invest.ally.com/v1/market/quotes.json?symbols={ticker}"

# 2: streaming stock:
session = Session()
r = Request(
    method="POST",
    url=stock_url,
    auth=auth,
)

req = session.prepare_request(r)
x = session.send(req, stream=True)
x.raise_for_status()


results = stream_request(x)
for r in results:
    print(r)
    
