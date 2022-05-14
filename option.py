import requests
import json
import pandas as pd
import numpy as np
from requests_oauthlib import OAuth1

ticker = 'rivn'

traditional = 60454723
individual = 60717214
roth = 60739817

consumer_key = 'X7gzjAOxOS9Pm8UfHxj6Ds73HRDO0fsaTkLVI5QdWyE6'
consumer_secret = 'Hjpdl7DVdChoP729RXUZ28SZPZdCUZObgVyn1k5ZJFM0'
oath_token = 'RIyCUWet7Zye3TLxf55zAkJ7QroPhsBm7bUJewi7B8I8'
oath_token_secret = '5cLiGd5kGXeV2mmM5XkTqLE50Ga6QNYlv20tD7HR4dg8'
# auth:
auth = OAuth1(consumer_key, consumer_secret, oath_token, oath_token_secret)

acct_url = "https://devapi.invest.ally.com/v1/accounts.json"



# GET market options:
order_url = f"https://devapi.invest.ally.com/v1/market/options/search.json?symbol={ticker}&query=xyear-eq%3A2020ANDput_call-eq%3Acall"
order_res = requests.get(order_url, auth=auth)
order_json = json.loads(order_res.content.decode('utf-8'))


# GET strike prices:
order_url = f"https://devapi.invest.ally.com/v1/market/options/strikes.json?symbol=aapl"
order_res = requests.get(order_url, auth=auth)
order_json = json.loads(order_res.content.decode('utf-8'))


# GET expirations prices:
order_url = f"https://devapi.invest.ally.com/v1/market/options/expirations.json?symbol=aapl"
order_res = requests.get(order_url, auth=auth)
order_json = json.loads(order_res.content.decode('utf-8'))



# POST option buy to open:
xml="""
<FIXML xmlns="http://www.fixprotocol.org/FIXML-5-0-SP2">
  <Order TmInForce="0" Typ="2" Side="1" Px="1.00" PosEfct="O" Acct="60454723">
    <Instrmt CFI="OC" SecTyp="OPT" MatDt="2020-05-18T00:00:00.000-05:00" StrkPx="7" Sym="F"/>
    <OrdQty Qty="1"/>
  </Order>
</FIXML>
"""

order_url = "https://devapi.invest.ally.com/v1/accounts/60454723/orders.json"
order_res = requests.post(order_url, data=xml, auth=auth)
order_json = json.loads(order_res.content.decode('utf-8'))


