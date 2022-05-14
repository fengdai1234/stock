import requests
import json
import pandas as pd
import numpy as np


api_token = 'f49ff35fdae7ffcdedaa7a5e091ef6af'
ticker = 'CTRM'

income_url = f"https://fmpcloud.io/api/v3/income-statement/{ticker}?apikey={api_token}"
balancesheet_url = f'https://fmpcloud.io/api/v3/balance-sheet-statement/{ticker}?period=quarter&apikey={api_token}'
cashflow_url = f'https://fmpcloud.io/api/v3/cash-flow-statement/{ticker}?period=quarter&apikey={api_token}'
api_profile = 'https://financialmodelingprep.com/api/v3/company/profile/{ticker}'            
financial_ratio_url = f'https://fmpcloud.io/api/v3/ratios/{ticker}?period=quarter&apikey={api_token}'


def get_account_info(api_url):

    response = requests.get(api_url)

    if response.status_code == 200:
        return json.loads(response.content.decode('utf-8'))
    else:
        return None

income = get_account_info(income_url)
balancesheet = get_account_info(balancesheet_url)
cashflow = get_account_info(cashflow_url)
financial_ratio = get_account_info(financial_ratio_url)

index = range(len(financial_ratio))

df = pd.DataFrame(financial_ratio, index =index) 
df = df.set_index('date')

df.to_excel(f'files/{ticker}_fr.xlsx')

df = pd.read_excel('ba_fr.xlsx')

assetturnover = df['assetTurnover']
import pandas as pd

import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np

