import requests
from django.utils.timezone import make_aware
from datetime import datetime
from .models import StockData
import time

ALPHA_VANTAGE_API_KEY = '4PG1EWDHVVB6KE4C'
BASE_URL = 'https://www.alphavantage.co/query'

def fetch_stock_data(symbol):
    try:
        params = {
            'function': 'TIME_SERIES_DAILY',
            'symbol': symbol,
            'outputsize': 'full',
            'apikey': ALPHA_VANTAGE_API_KEY
        }
        
        response = requests.get(BASE_URL, params=params)
        
        if response.status_code == 429:
            raise Exception("Rate limit exceeded. Please try again later.")
        
        if response.status_code != 200:
            raise Exception(f"Failed to fetch data: {response.status_code}")
        
        data = response.json().get('Time Series (Daily)', {})
        
        if not data:
            raise Exception(f"No data found for symbol {symbol}.")
        
        for date_str, values in data.items():
            date = make_aware(datetime.strptime(date_str, "%Y-%m-%d"))
            
            StockData.objects.update_or_create(
                symbol=symbol,
                timestamp=date,
                defaults={
                    'open_price': values['1. open'],
                    'close_price': values['4. close'],
                    'high_price': values['2. high'],
                    'low_price': values['3. low'],
                    'volume': values['5. volume'],
                }
            )
    
    except requests.exceptions.RequestException as e:
        raise Exception(f"Network error: {e}")
    except Exception as e:
        raise Exception(str(e))