
from requests_oauthlib import OAuth1
from func import AccountNumber, Secret
import requests
import json
import os
os.path
import sys
sys.path
from dotenv import load_dotenv
load_dotenv()

class Order:
    # trad, ind, roth
    def __init__(self,acct,ticker,strike,price,qty,CFI,side,type,PosEfct,SecTyp,date):
        self.auth = OAuth1(consumer_key, consumer_secret, oath_token, oath_token_secret)
        self.acct = acct
        self.ticker = ticker
        self.strike = strike
        self.price = price
        self.qty = qty
        self.CFI = CFI # OC : call, OP: put
        self.side = side # "1" ‐ Buy, "2" ‐ Sell, "5" ‐ Sell Short
        self.type =  type # "1" ‐ Market, "2" ‐ Limit", "3" ‐ Stop, or "4" - Stop Limit.
        self.PosEfct = PosEfct # option legs require and attribute of "O" for opening or "C" for closing.
        self.SecTyp = SecTyp # "CS" for common stock or "OPT" for option.
        self.date = date # e.g: '2022-03-18'


    def trade(self):
        # POST Buy limit order :
        xml=f"""<FIXML xmlns="http://www.fixprotocol.org/FIXML-5-0-SP2">
                        <Order TmInForce="0" Typ="{self.type}" Side="{self.side}" Px="{self.price}" PosEfct="{self.PosEfct}" Acct="{self.acct}">
                            <Instrmt CFI="{self.CFI}" SecTyp="{self.SecTyp}" MatDt="{self.date}T00:00:00.000-05:00" StrkPx="{self.strike}" Sym="{self.ticker}"/>
                            <OrdQty Qty="{self.qty}"/>
                        </Order>
                    </FIXML>"""
        

        order_url = f"https://devapi.invest.ally.com/v1/accounts/{self.acct}/orders.json"
        order_res = requests.post(order_url, data=xml, auth=self.auth)
        order_json = json.loads(order_res.content.decode('utf-8'))


        return order_res,order_json
