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


# POST Sell limit order :
def sell_limit(acct,qty,ticker,price,auth):
    sell_xml=f"""
    <FIXML xmlns="http://www.fixprotocol.org/FIXML-5-0-SP2">
    <Order TmInForce="0" Typ="2" Side="2" Px="{price}" Acct="{acct}">
        <Instrmt SecTyp="CS" Sym="{ticker}"/>
        <OrdQty Qty="{qty}"/>
    </Order>
    </FIXML>
    """
    order_url = f"https://devapi.invest.ally.com/v1/accounts/{acct}/orders.json"
    order_res = requests.post(order_url, data=sell_xml, auth=auth)
    order_json = json.loads(order_res.content.decode('utf-8'))

    return  order_res,order_json

def change_order(acct,qty,ticker,price,order_id,auth):
# POST Buy limit order :
    buy_xml=f"""
    <FIXML xmlns="http://www.fixprotocol.org/FIXML-5-0-SP2">
    <OrdCxlRplcReq TmInForce="0" Typ="2" Side="1" Px="{price}" Acct="{acct}" OrigID="{order_id}">
        <Instrmt SecTyp="CS" Sym="{ticker}"/>
        <OrdQty Qty="{qty}"/>
    </OrdCxlRplcReq>
    </FIXML>
    """
    order_url = f"https://devapi.invest.ally.com/v1/accounts/{acct}/orders.json"
    order_res = requests.post(order_url, data=buy_xml, auth=auth)

    order_json = json.loads(order_res.content.decode('utf-8'))
    
    return order_res,order_json


def cancel_order(acct,qty,ticker,order_id,auth):
# POST Buy limit order :
    cancel_xml=f"""
    <FIXML xmlns="http://www.fixprotocol.org/FIXML-5-0-SP2">
    <OrdCxlReq TmInForce="0" Typ="2" Side="1" Acct="{acct}" OrigID="{order_id}">
        <Instrmt SecTyp="CS" Sym="{ticker}"/>
        <OrdQty Qty="{qty}"/>
    </OrdCxlReq>
    </FIXML>
    """
    order_url = f"https://devapi.invest.ally.com/v1/accounts/{acct}/orders.json"
    order_res = requests.post(order_url, data=cancel_xml, auth=auth)

    order_json = json.loads(order_res.content.decode('utf-8'))
    
    return order_res,order_json


# POST Sell limit order :
def sell_limit(acct,qty,ticker,price,auth):
    sell_xml=f"""
    <FIXML xmlns="http://www.fixprotocol.org/FIXML-5-0-SP2">
    <Order TmInForce="0" Typ="2" Side="2" Px="{price}" Acct="{acct}">
        <Instrmt SecTyp="CS" Sym="{ticker}"/>
        <OrdQty Qty="{qty}"/>
    </Order>
    </FIXML>
    """
    order_url = f"https://devapi.invest.ally.com/v1/accounts/{acct}/orders.json"
    order_res = requests.post(order_url, data=sell_xml, auth=auth)
    order_json = json.loads(order_res.content.decode('utf-8'))

    return  order_res,order_json


def get_order_list(acct,auth):
    # status: 0 -> open, 2 -> success, 4 -> canceled, 8 -> rejected
    order_url = f"https://devapi.invest.ally.com/v1/accounts/{acct}/orders.json"
    order_res = requests.get(order_url, auth=auth)
    order_json = json.loads(order_res.content.decode('utf-8'))
    order_xml = order_json.get('response').get('orderstatus').get('order')
    
    order_list = []
    if len(order_xml) == 1:
        o = order_xml.get('fixmlmessage')
        root = et.fromstring(o)
        
        for child in root:
            order_dic = child.attrib
            order_dic.update(child[0].attrib)
            order_dic.update(child[1].attrib)
            order_dic.update(child[2].attrib)

            if order_dic.get('Txt') != 'Canceled by user':
                order_list.append(order_dic)
        
    elif len(order_xml) > 1:
        for order in order_xml:
            o = order.get('fixmlmessage') 
            root = et.fromstring(o)
        
            for child in root:
                order_dic = child.attrib
                order_dic.update(child[0].attrib)
                order_dic.update(child[1].attrib)
                order_dic.update(child[2].attrib)

                if order_dic.get('Txt') != 'Canceled by user':
                    order_list.append(order_dic)

    return order_list
