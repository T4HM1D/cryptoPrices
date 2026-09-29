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
    crypto_str = ','.join(crypto_list)
    currency_str = ','.join(currency_list)
    print(f'Getting data for {crypto_str}')
    response = requests.get(url, headers=headers, params={'ids': crypto_str, 'vs_currencies': currency_str})
    return response.json()


def create_csv(crypto_data):
    """
    Creates dataframe from the crypto data for each coin, then export it a csv file.
    """
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


if __name__ == '__main__':
    crypto_list = ['bitcoin', 'ethereum', 'solana']
    currency_list = ['gbp', 'usd', 'eur']
    
    get_and_create_coin_price_csv(crypto_list, currency_list)