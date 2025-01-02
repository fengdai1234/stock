
from requests_oauthlib import OAuth1
from func import 
 AccountNumber, Secret*
import requests
import json
import collections
from datetime import datetime, date

class Option:
    # %20: space in XML
    def __init__(self):
        self.auth = OAuth1(consumer_key, consumer_secret, oath_token, oath_token_secret)
        

    def search_option_strike(self,ticker):

        option_url = f"https://devapi.invest.ally.com/v1/market/options/strikes.json?symbol={ticker}"
        
        option_res = requests.get(option_url, auth=self.auth)
        option_strike_list = json.loads(option_res.content.decode('utf-8')).get('response').get('prices').get('price')
        
        return option_strike_list

    def search_option_expirations(self,ticker):

        option_url = f"https://devapi.invest.ally.com/v1/market/options/expirations.json?symbol={ticker}"
        option_res = requests.get(option_url, auth=self.auth)
        expirations_list = json.loads(option_res.content.decode('utf-8')).get('response').get('expirationdates').get('date')
        
        return expirations_list

    # GET market quotes:use .json not xml , xml is a mess
    # date format: '20220318'
    def search_option_quotes(self,ticker,xdate,strike,put_call):
        # option_url = f"https://devapi.invest.ally.com/v1/market/options/search.json?symbol={ticker}&query=xyear-eq%3A{year}%20AND%20xmonth-eq%3A{month}%20AND%20strikeprice-eq%3A{strike}%20AND%20pull_call%3A{type}"
        option_url = f"https://devapi.invest.ally.com/v1/market/options/search.json?symbol={ticker}&query=xdate-eq%3A{xdate}%20AND%20strikeprice-eq%3A{strike}%20AND%20put_call%3A{put_call}"
        option_res = requests.get(option_url, auth=self.auth)
        option_list = json.loads(option_res.content.decode('utf-8')).get('response').get('quotes').get('quote')

        return option_list
        
        # 1.3: find upcoming expire date
    def get_close_exp_date(self,ticker,close_order):
        expiration_list = self.search_option_expirations(ticker)
        # get all differences with date as values 
        expiration_datelist = [datetime.strptime(dat, '%Y-%m-%d').date()for dat in expiration_list]
        cloz_dict = {dat - date.today(): dat  for dat in expiration_datelist}
        # extracting minimum key using min()
        ordered_cloz_date = collections.OrderedDict(cloz_dict.items())
        # 1.3.2: get the second nearest exp date:
        closest_exp_date = cloz_dict[list(ordered_cloz_date.keys())[close_order]]

        # printing result
        print("second Nearest date from list : " + str(closest_exp_date))
        close_exp_date = closest_exp_date.strftime('%Y%m%d')
        # close_exp_date = '20220617'
        
        return close_exp_date

