
from requests_oauthlib import OAuth1
from func.credentials import *
import requests
import json

# GET streaming quotes: stream only return when there is changes in real price?
class Quote:
    # %20: space in XML
    def __init__(self):
        self.auth = OAuth1(consumer_key, consumer_secret, oath_token, oath_token_secret)

    def get_streming_quotes(self,ticker):
        quotes_url = f"https://devapi-stream.invest.ally.com/v1/market/quotes.json?symbols={ticker}"
        quotes_res = requests.get(quotes_url, auth=self.auth)
        streming_quotes = json.loads(quotes_res.content.decode('utf-8'))

        return streming_quotes
    
    def timesales(self,ticker,startdate,enddate):
        
        # /v1/market/timesales.xml?symbols=AAPL&startdate=2012-04-06&interval=1min
        quotes_url = f"https://devapi.invest.ally.com/v1/market/timesales.json?symbols={ticker}&startdate={startdate}&enddate={enddate}"
        quotes_res = requests.get(quotes_url, auth=self.auth)
        time_sales = json.loads(quotes_res.content.decode('utf-8')).get('response').get('quotes').get('quote')

        return time_sales
    