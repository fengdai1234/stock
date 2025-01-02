
from requests_oauthlib import OAuth1
from func import AccountNumber, Secret
import requests
import json
from datetime import date, timedelta
import os
import sys
sys.path


# GET streaming quotes: stream only return when there is changes in real price?
class Quote:
    # %20: space in XML
    def __init__(self):
        self.auth = OAuth1(consumer_key, consumer_secret, oath_token, oath_token_secret)

    def get_streaming_quotes(self,ticker):
        quotes_url = f"https://devapi-stream.invest.ally.com/v1/market/quotes.json?symbols={ticker}"
        quotes_res = requests.get(quotes_url, auth=self.auth)
        streming_quotes = json.loads(quotes_res.content.decode('utf-8'))

        yield streming_quotes
    
    def timesales(self,ticker,startdate,enddate):
        
        # /v1/market/timesales.xml?symbols=AAPL&startdate=2012-04-06&interval=1min
        quotes_url = f"https://devapi.invest.ally.com/v1/market/timesales.json?symbols={ticker}&startdate={startdate}&enddate={enddate}"
        quotes_res = requests.get(quotes_url, auth=self.auth)
        time_sales = json.loads(quotes_res.content.decode('utf-8')).get('response').get('quotes').get('quote')

        return time_sales

    def get_last_price(self,ticker):
        today = date.today().strftime('%Y-%m-%d')
        tmr = (date.today() - timedelta(-1)).strftime('%Y-%m-%d')
        time_sales = self.timesales(ticker,today,tmr)
        last_price = float(time_sales[-1].get('last'))
        
        return last_price

    #  1.2.2: find yesteraday's last sale
    def get_yesterday_close_price(self,ticker):
        yesterday = (date.today() - timedelta(1)).strftime('%Y-%m-%d')
        today = date.today().strftime('%Y-%m-%d')
        # datetime.strptime(today, '%Y-%m-%d').date()
        time_sales = self.timesales(ticker,yesterday,today)
        yesterday_close_price = float(time_sales[-1].get('last'))
        
        return yesterday_close_price