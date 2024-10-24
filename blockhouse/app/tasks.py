import requests
from django.utils.timezone import make_aware
from datetime import datetime, timedelta
from .models import StockData
import time

ALPHA_VANTAGE_API_KEY = 'your_api_key_here'
BASE_URL = 'https://www.alphavantage.co/query'
RETRY_DELAY = 60  # Wait 60 seconds before retrying after hitting rate limit
MAX_RETRIES = 3  # Maximum retries for network issues

def fetch_stock_data(symbol):
    params = {
        'function': 'TIME_SERIES_DAILY',
        'symbol': symbol,
        'outputsize': 'full',  # Fetch the full data
        'apikey': ALPHA_VANTAGE_API_KEY
    }

    retries = 0
    while retries < MAX_RETRIES:
        try:
            # Make the API request
            response = requests.get(BASE_URL, params=params)
            
            # Handle rate limiting (HTTP 429)
            if response.status_code == 429:
                print(f"Rate limit exceeded. Retrying in {RETRY_DELAY} seconds...")
                time.sleep(RETRY_DELAY)  # Sleep for 60 seconds and retry
                continue

            # Raise an exception for any other non-successful status code
            if response.status_code != 200:
                response.raise_for_status()

            # Parse the JSON response
            data = response.json().get('Time Series (Daily)', {})

            if not data:
                raise Exception(f"No data found for symbol {symbol}.")

            # Get the current date and calculate the date two years ago
            today = datetime.now()
            two_years_ago = today - timedelta(days=2 * 365)

            # Iterate through the daily data
            for date_str, values in data.items():
                # Convert date string to datetime object
                date = datetime.strptime(date_str, "%Y-%m-%d")
                
                # Only process data within the last two years
                if date >= two_years_ago:
                    # Make the date timezone aware
                    date = make_aware(date)
                    
                    # Store or update the stock data in the database
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
            print(f"Data for {symbol} from the last two years fetched successfully.")
            break  # Exit the retry loop if successful

        except requests.exceptions.RequestException as e:
            # Handle network issues (e.g., connection error, timeout)
            retries += 1
            print(f"Network error: {e}. Retrying... ({retries}/{MAX_RETRIES})")
            if retries == MAX_RETRIES:
                raise Exception(f"Failed to fetch data for {symbol} after {MAX_RETRIES} retries.")
        
        except Exception as e:
            # Handle other unexpected errors (e.g., no data, bad response)
            raise Exception(f"An error occurred: {str(e)}")