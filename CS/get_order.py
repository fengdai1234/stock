import requests
import json
from requests_oauthlib import OAuth1
from func.credentials import *
from func.orderfunc import get_order_list
# auth:
auth = OAuth1(consumer_key, consumer_secret, oath_token, oath_token_secret)
account_type = trad

# TODO: get open order and current price of the stock, 
order_list = get_order_list(account_type,auth)
len(order_list)
order_list[3]

# TODO: how to find the info for the order?
acct = account_type
order_url = f"https://devapi.invest.ally.com/v1/accounts/{acct}/orders.json"
order_res = requests.get(order_url, auth=auth)
order_json = json.loads(order_res.content.decode('utf-8'))
len(order_json)

order_xml = order_json.get('response').get('orderstatus').get('order')



len(order_xml)
order_xml[0].get('fixmlmessage')
import xml.etree.ElementTree as et
o = order_xml[0].get('fixmlmessage')
root = et.fromstring(o)

root.tag
for child in root:
    order_dic = child.attrib
    print(order_dic)

root.attrib

root[0].attrib
root[0][0].attrib
root[0][1].attrib
root[0][2].attrib




order_list = []
for order in order_xml:
    o = order.get('fixmlmessage') 
    root = et.fromstring(o)

    for child in root:
        order_dic = child.attrib
        # add sticker info
        order_dic.update(child[0].attrib)
        order_dic.update(child[1].attrib)
        order_dic.update(child[2].attrib)
        
        if order_dic.get('Txt') != 'Canceled by user':
            order_list.append(order_dic)
            