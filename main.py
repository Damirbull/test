import pandas as pd
import numpy as np
import requests
import time



def get_futures_data():
    url = 'https://fapi.binance.com/futures/data/fundingRate?symbol=ETHUSDT&limit=100'

    response = requests.get(url)
    df = pd.DataFrame(response.json())
    df['fundingRate'] = df['fundingRate'].astype(float)
    df['fundingTime'] = pd.to_datetime(df['fundingTime'], unit='ms')
    df.set_index('fundingTime', inplace=True)
    df.sort_index(inplace=True)
    return df

def holt_winters_filter(series, alpha=0.5, beta=0.5):
    level = np.array([series[0]])
    trend = np.array([series[1] - series[0]])
    for i in range(1, len(series)):
        level = np.append(level, alpha * series[i] + (1 - alpha) * (level[i - 1] + trend[i - 1]))
        trend = np.append(trend, beta * (level[i] - level[i - 1]) + (1 - beta) * trend[i - 1])
    return level + trend

print("Программа запущена. Ожидание изменения цены...")


