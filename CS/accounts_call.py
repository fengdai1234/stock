import requests
import json
import pandas as pd
import numpy as np
from requests_oauthlib import OAuth1
from func.credentials import *

acct = roth
ticker = 'BABA'

# auth:
auth = OAuth1(consumer_key, consumer_secret, oath_token, oath_token_secret)
acct_url = "https://devapi.invest.ally.com/v1/accounts.json"
acct_res = requests.get(acct_url, auth=auth)
acct_json = json.loads(acct_res.content.decode('utf-8'))


# get all account holding info
# 1: traditional acct: 0 in the list
acct_pos_list = acct_json.get('response').get('accounts').get('accountsummary')
acct_pos_list[0].keys()
acct_num = acct_pos_list[0].get('account')

acct_pos_list[0].get('accountbalance').keys()
acct_pos_list[0].get('accountbalance').get('accountvalue')
acct_pos_list[0].get('accountbalance').get('fedcall')
acct_pos_list[0].get('accountbalance').get('housecall')
acct_pos_list[0].get('accountbalance').get('money')

buyingpower = acct_pos_list[0].get('accountbalance').get('buyingpower')
# buying power of this acct
cash = buyingpower.get('cashavailableforwithdrawal')
daytrading = buyingpower.get('daytrading')

# Holding value for each cagtegory
security = acct_pos_list[0].get('accountbalance').get('securities')
security.get('longoptions')
security.get('longstocks')

# get acct activity history:
hist_url = f"https://devapi.invest.ally.com/v1/accounts/{acct}/history.xml"


acct_pos_list[0].get('accountholdings')
len(acct_pos_list)

acct_json.get('response').get('accounts').keys()


# 2: roth acct
acct_pos_list[2].get('account')
acct_pos_list[1].get('accountbalance')


# GET accounts balances:
acct_bal_url = "https://devapi.invest.ally.com/v1/accounts/balances.json"
bal_res = requests.get(acct_bal_url, auth=auth)
bal_json = json.loads(bal_res.content.decode('utf-8'))
bal_json.get('response').get('accountbalance')

# GET market clock:
market_clock = f"https://devapi.invest.ally.com/v1/market/clock.json"
order_res = requests.get(market_clock, auth=auth)
market_clock_json = json.loads(order_res.content.decode('utf-8'))
market_clock_json.get('response').get('status')


# GET market news:
market_news = f"https://devapi.invest.ally.com/v1/market/news/search.json?symbols={ticker}&maxhits=15"
market_news_res = requests.get(market_news, auth=auth)
market_news_json = json.loads(market_news_res.content.decode('utf-8'))
news_id = market_news_json.get('response').get('articles').get('article')[0].get('id')
news_id
# GET market news by ID:

news_url = f"https://devapi.invest.ally.com/v1/market/news/{news_id}.json"
news_res = requests.get(news_url, auth=auth)
news_json = json.loads(news_res.content.decode('utf-8'))
news_json


# GET market topvolume:
topv_url = f"https://devapi.invest.ally.com/v1/market/toplists/topvolume.json?exchange=A"
topv_res = requests.get(topv_url, auth=auth)
topv_json = json.loads(topv_res.content.decode('utf-8'))
topv_json

# GET WATCHLIST:
wl_url = f"https://devapi.invest.ally.com/v1/watchlists.json"
wl_res = requests.get(wl_url, auth=auth)
wl_json = json.loads(order_res.content.decode('utf-8'))
wl_json

# GET watchlist:id:
order_url = f"https://devapi.invest.ally.com/v1/watchlists/DEFAULT.json"
order_res = requests.get(order_url, auth=auth)
order_json = json.loads(order_res.content.decode('utf-8'))


def get_account_info(api_url):

    response = requests.get(api_url)

    if response.status_code == 200:
        return json.loads(response.content.decode('utf-8'))
    else:
        return None