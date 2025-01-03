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
from func.orderfunc import  get_order_list, cancel_order
from func.option import Option
from func.quote import Quote
from func.orderfunc import get_order_list, cancel_order
from datetime import datetime, timezone, date, timedelta
import pytz
import collections
from func.utility import closest_value

# trad, ind, roth
# 1.get option expiration date and strike price
auth = OAuth1(consumer_key, consumer_secret, oath_token, oath_token_secret)
ticker = 'EDU'
put_call = 'put'
# strike_date = '20220506'
# strike = '100'

# 1.1:get market quotes for a stock
quote = Quote()
# quote.get_yesterday_close_price(ticker)
# TODO: beginning of the day, there is [-1]
# last_price = quote.get_last_price(ticker)
quote.timesales(ticker,date.today().strftime('%Y-%m-%d'),(date.today() - timedelta(-1)).strftime('%Y-%m-%d'))

last_price = quote.get_yesterday_close_price(ticker)
last_price = 19

# 1.2: figure out near the money strike price
# 1.2.1: get option strike list to int
option  = Option()
strike_list = option.search_option_strike(ticker)
strike_int_list = [(float(i)) for i in strike_list]

 
# TODO: how to get the premarket price
closest_strike=closest_value(strike_int_list,last_price)
print("The closest value to the "+ str(last_price)+" is",closest_strike)
# closest_strike = 114


# 1.3: get the close exp date:
close_exp_date = option.get_close_exp_date(ticker,1)

option_quotes = option.search_option_quotes(ticker=ticker,strike=closest_strike,xdate=close_exp_date,put_call=put_call)
option_quotes


# 1.3:
# strike_list = ['105','106','107']
acct = roth

# for strike in strike_list:

#     option  = Option()
#     option_quotes = option.search_option_quotes(ticker=ticker,strike=strike,xdate=strike_date,put_call=put_call)
#     option_quotes

    # middle_price = round((float(option_quotes.get('bid')) + float(option_quotes.get('ask')))/2,2)

    # len(option_quotes)
# option_quotes.keys()
# 3.get today's order list

order_list = get_order_list(acct=acct,auth=auth)
valid_orders = [order for order in order_list if order.get('Stat') not in ('4','8')]
valid_orders

# 2. trade buy call option
put_call = 'pul'
qty = '10'
CFI = 'OC' # OC : call, OP: put
side = '2' # "1" ‐ Buy, "2" ‐ Sell, "5" ‐ Sell Short
type =  '2' # "1" ‐ Market, "2" ‐ Limit", "3" ‐ Stop, or "4" - Stop Limit.
# limit_price = '1.07'
# limit_price = (float(option_quotes.get('ask')) + float(option_quotes.get('bid')))/2
# limit_price = 5
# limit_price=3.95
PosEfct = 'O' # option legs require and attribute of "O" for opening or "C" for closing.
SecTyp = 'OPT' # "CS" for common stock or "OPT" for option.
# TODO: convert date to format below:
execute_date = date.strftime(datetime.strptime(close_exp_date,'%Y%m%d'),'%Y-%m-%d')
# execute_date = '2022-06-10'

option_order = Order(
                acct = acct,
                ticker=ticker,
                qty=qty,
                price=limit_price,
                strike=closest_strike,
                CFI=CFI,
                side=side,
                type=type,
                PosEfct = PosEfct ,
                SecTyp = SecTyp,
                date = execute_date)
option_order.trade()

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
current_order = get_order_list(acct=roth,auth=auth)
len(current_order)
current_order
current_order[0]
current_order[1]['OrdID']
current_order[0]


cancel_order(roth,10,ticker,current_order[1]['OrdID'],auth)



# 61*0.25 + 62*0.25 + 84*0.15 + 73*0.1+ 62*0.1 + 93*0.15

