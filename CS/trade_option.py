# https://www.ally.com/api/invest/documentation/trading/
# side = 1: buy, side = 2, sell
# typ = 1: market order, typ =2 : limit order
# TmInForce=0: day order, TmInForce=1: GTC (60days)
import requests
import json
import pandas as pd
import numpy as np
from requests_oauthlib import OAuth1
import xml.etree.ElementTree as et
from func.credentials import *
from func.order import Order, Quote
from func.orderfunc import get_order_list, cancel_order


# trad, ind, roth
# 1.get quotes
auth = OAuth1(consumer_key, consumer_secret, oath_token, oath_token_secret)
ticker = 'baba'
order_date = '20220506'
put_call = 'call'
strike = '100'

quote  = Quote()
option_quotes = quote.get_opt_quotes(ticker=ticker,strike=strike,xdate=order_date,put_call=put_call)
option_quotes

strike_list = ['100','101','102']
acct = trad

for strike in strike_list:

    quote  = Quote()
    option_quotes = quote.get_opt_quotes(ticker=ticker,strike=strike,xdate=order_date,put_call=put_call)
    option_quotes

    # middle_price = round((float(option_quotes.get('bid')) + float(option_quotes.get('ask')))/2,2)


    # len(option_quotes)
    # option_quotes.keys()
    # 2. trade buy call option
    qty = '10'
    CFI = 'OC' # OC : call, OP: put
    side = '1' # "1" ‐ Buy, "2" ‐ Sell, "5" ‐ Sell Short
    type =  '2' # "1" ‐ Market, "2" ‐ Limit", "3" ‐ Stop, or "4" - Stop Limit.
    # limit_price = '1.07'
    limit_price = option_quotes.get('ask')
    PosEfct = 'O' # option legs require and attribute of "O" for opening or "C" for closing.
    SecTyp = 'OPT' # "CS" for common stock or "OPT" for option.
    execute_date = '2022-05-06'

    option = Order( acct = acct,
                    ticker=ticker,
                    qty=qty,
                    price=limit_price,
                    strike=strike,
                    CFI=CFI,
                    side=side,
                    type=type,
                    PosEfct = PosEfct ,
                    SecTyp = SecTyp,
                    date = execute_date)
    option.trade()

# option = option_list[0]
option_quotes.get('bid')
option_quotes.get('ask')
option_quotes.get('strikeprice')
option_quotes.get('secclass')
option_quotes.get('put_call')
option_quotes.get('pvol')
option_quotes.get('chg')
option_quotes.get('cl')
option_quotes.get('exch')
option_quotes.get('exch_desc')
option_quotes.get('hi')
option_quotes.get('op_flag')
option_quotes.get('opn')
option_quotes.get('xdate')

# 3. get the current option orders:
current_order = get_order_list(acct=ind,auth=auth)
len(current_order)
current_order
current_order[0]
current_order[0]['OrdID']
current_order[0]


# 61*0.25 + 62*0.25 + 84*0.15 + 73*0.1+ 62*0.1 + 93*0.15