import requests
import json
import pandas as pd
import numpy as np
from requests_oauthlib import OAuth1
from func.credentials import *
# auth:
auth = OAuth1(consumer_key, consumer_secret, oath_token, oath_token_secret)

# order_json = json.loads(order_res.content.decode('utf-8'))
# print(order_json)
account_type = roth

def  sell_limit_all(account_type):
  # get all the asking prices now
  url = f"https://devapi.invest.ally.com/v1/accounts/{account_type}.json"
  res = requests.get(url, auth=auth)
  holding = json.loads(res.content.decode('utf-8')).get('response').get('accountholdings').get('holding')
  print(f"number of stocks holding: {len(holding)}")
  
  for i in range(len(holding)):
  # for loop:
    qty = holding[i].get('displaydata').get('qty')
    try:
      qty = int(qty)
    except :
      print("quantity of stock must be int!") 
      continue
    
    lastprice = float(holding[i].get('displaydata').get('lastprice').strip('$,'))
    selllimit = round(lastprice*1.05,2)
    ticker = holding[i].get('displaydata').get('symbol')

  # POST Sell limit order :
    xml = f"""
    <FIXML xmlns="http://www.fixprotocol.org/FIXML-5-0-SP2">
        <Order TmInForce="0" Typ="2" Side="2" Px="{selllimit}" Acct="{account_type}">
            <Instrmt SecTyp="CS" Sym="{ticker}"/>
            <OrdQty Qty="{qty}"/>
        </Order>
    </FIXML>
    """

    order_url = f"https://devapi.invest.ally.com/v1/accounts/{account_type}/orders.json"
    order_res = requests.post(order_url, data=xml, auth=auth)
    order_json = json.loads(order_res.content.decode('utf-8'))
    print(order_json)

  return None

# sell_limit_all(roth)
sell_limit_all(ind)


# get all orders:


import xml.etree.ElementTree as et
root = et.fromstring(order0)
for child in root:
  print(child.tag)

# POST cancel order:
xml="""
<FIXML xmlns="http://www.fixprotocol.org/FIXML-5-0-SP2">
  <OrdCxlReq TmInForce="0" Typ="2" Side="1" OrigID="SVI-6098692977/2" Acct="60454723">
    <Instrmt SecTyp="CS" Sym="F"/>
    <OrdQty Qty="1"/>
  </OrdCxlReq>
</FIXML>
"""
