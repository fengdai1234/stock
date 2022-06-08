# https://www.ally.com/api/invest/documentation/trading/
# side = 1: buy, side = 2, sell
# typ = 1: market order, typ =2 : limit order
# TmInForce=0: day order, TmInForce=1: GTC (60days)
import requests
import json
import pandas as pd
import numpy as np
from requests_oauthlib import OAuth1
from func.credentials import *
import xml.etree.ElementTree as et
from func.orderfunc import buy_limit,get_quotes,get_order_list,cancel_order

# trad, ind, roth
auth = OAuth1(consumer_key, consumer_secret, oath_token, oath_token_secret)
acct = ind
ticker = 'rivn'
strike = '41'
price = '1.0'
qty = '1'
CFI = 'OC' # OC : call, OP: put
side = '1' # "1" ‐ Buy, "2" ‐ Sell, "5" ‐ Sell Short
type =  '2' # "1" ‐ Market, "2" ‐ Limit", "3" ‐ Stop, or "4" - Stop Limit.
PosEfct = 'O' # option legs require and attribute of "O" for opening or "C" for closing.
SecTyp = 'OPT' # "CS" for common stock or "OPT" for option.




def buy_limit(acct,qty,ticker,price,auth):
# POST Buy limit order :
    buy_xml=f"""
    <FIXML xmlns="http://www.fixprotocol.org/FIXML-5-0-SP2">
    <Order TmInForce="0" Typ="2" Side="1" Px="{price}" Acct="{acct}">
        <Instrmt SecTyp="CS" Sym="{ticker}"/>
        <OrdQty Qty="{qty}"/>
    </Order>
    </FIXML>
    """

    order_url = f"https://devapi.invest.ally.com/v1/accounts/{acct}/orders.json"
    order_res = requests.post(order_url, data=buy_xml, auth=auth)

    order_json = json.loads(order_res.content.decode('utf-8'))


    return order_res,order_json

# trad, ind, roth
auth = OAuth1(consumer_key, consumer_secret, oath_token, oath_token_secret)


quotes = get_quotes(ticker,auth)
bid_p = quotes.get('bid')


order_res, order_json = buy_limit(ind,qty=100,ticker=ticker,price=bid_p,auth=auth)
# order_res, order_json = sell_limit(ind,qty=100,ticker='ctrm',price=ask_p)

order_list = get_order_list(ind,auth)

# cancel_order(ind,qty=100,ticker=ticker,order_id = order_list[0].get('ID'),auth=auth)



# order_url = f"https://devapi.invest.ally.com/v1/accounts/{acct}/orders.json"
# order_res = requests.get(order_url, auth=auth)
# order_json = json.loads(order_res.content.decode('utf-8'))
# order_xml = order_json.get('response').get('orderstatus').get('order')
# order_list = []

# for order in order_xml:
#     o = order.get('fixmlmessage') 
#     root = et.fromstring(o)

#     for child in root:
#         order_dic = child.attrib
#         if order_dic.get('Txt') != 'Canceled by user':
#             order_list.append(order_dic)

