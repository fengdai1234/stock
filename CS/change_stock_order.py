import requests
import json
import pandas as pd
import numpy as np
from requests_oauthlib import OAuth1
from func.credentials import *

from func.orderfunc import change_order,cancel_order, get_order_list

# trad, ind, roth
auth = OAuth1(consumer_key, consumer_secret, oath_token, oath_token_secret)
ticker = 'baba'
acct = ind

order_list = get_order_list(ind,auth)
order_list
order_id = order_list[0].get('ID')

# change_order(acct,qty,ticker,price,order_id,auth=auth)
change_order(ind,qty=100,ticker='ctrm',price=0.1,order_id = order_id,auth=auth)
cancel_order(ind,qty=100,ticker='ctrm',order_id = order_id,auth=auth)

