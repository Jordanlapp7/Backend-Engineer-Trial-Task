from django.http import JsonResponse
from .models import StockData, PredictedStockPrice
from .ml import load_pretrained_model, predict_stock_prices
from .tasks import fetch_stock_data
from .backtest import generate_performance_summary
import pandas as pd

def fetch_data_view(request, symbol):
    try:
        fetch_stock_data(symbol)
        return JsonResponse({"status": "success", "message": f"Data for {symbol} fetched successfully."})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})
    
def backtest_view(request, symbol, initial_investment):
    try:
        summary = generate_performance_summary(symbol, float(initial_investment))
        return JsonResponse({"status": "success", "summary": summary})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})
    
# API to predict future stock prices
def predict_stock_prices_api(request, symbol):
    # Load the pre-trained model
    model = load_pretrained_model()

    # Fetch historical stock data for the symbol
    stock_data = StockData.objects.filter(symbol=symbol).order_by('timestamp')

    # Convert to a Pandas DataFrame for prediction
    data = pd.DataFrame(list(stock_data.values('timestamp', 'close_price')))
    data['timestamp'] = pd.to_datetime(data['timestamp'])
    data.set_index('timestamp', inplace=True)

    # Ensure there is enough historical data for prediction
    if len(data) < 50:
        return JsonResponse({'status': 'error', 'message': 'Not enough historical data to make predictions.'}, status=400)

    # Predict stock prices for the next 30 days
    try:
        predictions = predict_stock_prices(model, data)
    except ValueError as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

    # Store predictions in the database
    for _, row in predictions.iterrows():
        PredictedStockPrice.objects.update_or_create(
            symbol=symbol,
            date=row['date'],
            defaults={'predicted_price': row['predicted_price']}
        )

    # Return predictions as JSON response
    return JsonResponse({
        'status': 'success',
        'predictions': predictions.to_dict(orient='records')
    })