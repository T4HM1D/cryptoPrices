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
    return crypto_data


def read_csv(coins):
    dfs = {}
    for coin in coins:
        try:
            print(f'Reading {coin}.csv...')
            df = pd.read_csv(f'{coin}.csv')
            dfs[coin] = df
        except:
            print(f'{coin}.csv not found')
    return dfs

def merge_data(dataframes):
    formatted_dfs = []  
    print('Merging Dataframes...')
    for coin, df in dataframes.items():
        formatted_dfs.append(df.rename(columns={'price': coin}))

    dfs = [df.set_index('currency') for df in formatted_dfs]
    merged_dfs = pd.concat(dfs, axis = 1)
    print('Merged Dataframe successful')
    return merged_dfs

def get_highest_and_lowest_coins(df, currency):
    row = df.loc[currency]

    highest_price = row.max()
    highest_coin = row.idxmax()

    lowest_price = row.min()
    lowest_coin = row.idxmin()
    print(f'Calculating highest and lowest priced coin in {currency}:')
    return {'currency': currency,
            'highest': {'coin': highest_coin, 'price': float(highest_price)},
            'lowest': {'coin': lowest_coin, 'price': float(lowest_price)}
            }

def cal_avg_price(df, currency):
    row = df.loc[currency]
    avg_price = row.mean()
    print(f'Calculating average {currency} price accross all coins:')
    return {f'average price in {currency}': float(avg_price)}


if __name__ == '__main__':
    crypto_list = ['bitcoin', 'ethereum', 'solana']
    currency_list = ['gbp', 'usd', 'eur']
    
    print(get_and_create_coin_price_csv(crypto_list, currency_list))

    dfs = read_csv(crypto_list)
    merged_df = merge_data(dfs)

    print(get_highest_and_lowest_coins(merged_df, 'gbp'))
    print(cal_avg_price(merged_df, 'gbp'))