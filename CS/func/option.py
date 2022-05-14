
from requests_oauthlib import OAuth1
from func.credentials import *
import requests
import json

class Option:
    # %20: space in XML
    def __init__(self):
        self.auth = OAuth1(consumer_key, consumer_secret, oath_token, oath_token_secret)
        
    # GET market quotes:use .json not xml , xml is a mess
    # date format: '20220318'
    def search_option_quotes(self,ticker,xdate,strike,put_call):
        # option_url = f"https://devapi.invest.ally.com/v1/market/options/search.json?symbol={ticker}&query=xyear-eq%3A{year}%20AND%20xmonth-eq%3A{month}%20AND%20strikeprice-eq%3A{strike}%20AND%20pull_call%3A{type}"
        option_url = f"https://devapi.invest.ally.com/v1/market/options/search.json?symbol={ticker}&query=xdate-eq%3A{xdate}%20AND%20strikeprice-eq%3A{strike}%20AND%20put_call%3A{put_call}"
        option_res = requests.get(option_url, auth=self.auth)
        option_list = json.loads(option_res.content.decode('utf-8')).get('response').get('quotes').get('quote')

        return option_list

    def search_option_strike(self,ticker,xdate,strike,put_call):

        option_url = f"https://devapi.invest.ally.com/v1/market/options/search.json?symbol={ticker}&query=xdate-eq%3A{xdate}%20AND%20strikeprice-eq%3A{strike}%20AND%20put_call%3A{put_call}"
        option_res = requests.get(option_url, auth=self.auth)
        option_list = json.loads(option_res.content.decode('utf-8')).get('response').get('quotes').get('quote')

        
        return option_strike_list

