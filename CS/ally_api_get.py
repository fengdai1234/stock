import requests
import json
import pandas as pd
import numpy as np
from requests_oauthlib import OAuth1
from func.credentials import *

ticker = 'BA'

# auth:
auth = OAuth1(consumer_key, consumer_secret, oath_token, oath_token_secret)
acct_url = "https://devapi.invest.ally.com/v1/accounts.json"
acct_res = requests.get(acct_url, auth=auth)
acct_json = json.loads(acct_res.content.decode('utf-8'))

acct_json.get('response').get('error') 
acct_json.get('response').get('@id')
acct_json.get('response').get('elapsedtime')

# get all account holding info
acct_pos_list = acct_json.get('response').get('accounts').get('accountsummary')
type(acct_pos_list)
len(acct_pos_list)
acct_pos_list[0]


# GET balances:
acct_bal_url = "https://devapi.invest.ally.com/v1/accounts/balances.json"
bal_res = requests.get(acct_bal_url, auth=auth)
bal_json = json.loads(bal_res.content.decode('utf-8'))
bal_json.get('response')

# GET market clock:
order_url = f"https://devapi.invest.ally.com/v1/market/clock.json"
order_res = requests.get(order_url, auth=auth)
order_json = json.loads(order_res.content.decode('utf-8'))


# GET market news:
order_url = f"https://devapi.invest.ally.com/v1/market/news/search.json?symbols=ctrm&maxhits=15"
order_res = requests.get(order_url, auth=auth)
order_json = json.loads(order_res.content.decode('utf-8'))

# GET market news by ID:
order_url = f"https://devapi.invest.ally.com/v1/market/news/2938-A2129695-58CDJP0V9UE1SGUS51R8UJH178.json"
order_res = requests.get(order_url, auth=auth)
order_json = json.loads(order_res.content.decode('utf-8'))

# GET market timesales prices:
order_url = f"https://devapi.invest.ally.com/v1/market/timesales.json?symbols=aapl&startdate=2020-03-20"
order_res = requests.get(order_url, auth=auth)
order_json = json.loads(order_res.content.decode('utf-8'))

# GET market topvolume:
order_url = f"https://devapi.invest.ally.com/v1/market/toplists/topvolume.json?exchange=A"
order_res = requests.get(order_url, auth=auth)
order_json = json.loads(order_res.content.decode('utf-8'))

# GET WATCHLIST:
order_url = f"https://devapi.invest.ally.com/v1/watchlists.json"
order_res = requests.get(order_url, auth=auth)
order_json = json.loads(order_res.content.decode('utf-8'))

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