import requests
import pandas as pd
import os 
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('API_KEY')

def get_crypto_data(crypto_list, currency_list):
    """
    Fetches cryptocurrency prices for the specified cryptocurrencies and currencies.
    args:
        crypto_list (list): List of cryptocurrency IDs (e.g., ['bitcoin', 'ethereum']).
        currency_list (list): List of currency codes (e.g., ['usd', 'eur']).
    returns:
        dict: A dictionary containing cryptocurrency prices for the specified currencies.
    """
    print('Fetching cryptocurrency data...')
    url = 'https://api.coingecko.com/api/v3/simple/price'

    headers = {
        'x-cg-demo-api-key': api_key
    }
    crypto_data = {}
    for crypto in crypto_list:
        print(f'getting data for {crypto}')
        response = requests.get(url, headers=headers, params={'ids': crypto, 'vs_currencies': ','.join(currency_list)})
        if response.status_code == 200:
            print(f'Successfully fetched data for {crypto}')
            crypto_data[crypto] = response.json()[crypto]
        else:
            print(f'Error fetching data for {crypto}: {response.status_code}')
    return crypto_data


def create_csv(crypto_data):
    dataframes = {}
    for coin, prices in crypto_data.items():
        df = pd.DataFrame(prices.items(), columns=['currency', 'price'])
        dataframes[coin] = df

    for coin, df in dataframes.items():
        filename = f'{coin}.csv'
        df.to_csv(filename, index=False)
        print(f'{filename} saved successfully')


def get_and_create_coin_price_csv(crypto_list, currency_list):
    crypto_data = get_crypto_data(crypto_list, currency_list)
    create_csv(crypto_data)


crypto_list = ['bitcoin', 'ethereum', 'solana']
currency_list = ['gbp', 'usd', 'eur']

print(get_and_create_coin_price_csv(crypto_list, currency_list))