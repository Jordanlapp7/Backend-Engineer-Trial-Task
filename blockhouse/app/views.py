from django.http import JsonResponse, FileResponse
from .models import StockData, PredictedStockPrice
from .reports import calculate_backtest_metrics, generate_stock_price_plot, generate_pdf_report
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

# Django view for generating the report
def generate_report(request, symbol):
    # Fetch actual and predicted data for the stock
    actual_data = StockData.objects.filter(symbol=symbol).order_by('timestamp')
    predicted_data = PredictedStockPrice.objects.filter(symbol=symbol).order_by('date')
    
    # Convert to DataFrame
    actual_df = pd.DataFrame(list(actual_data.values('timestamp', 'close_price')))
    predicted_df = pd.DataFrame(list(predicted_data.values('date', 'predicted_price')))
    
    # Calculate metrics (replace with actual backtest data if necessary)
    metrics = calculate_backtest_metrics({
        'final_portfolio_value': 15000,  # Example value, replace with actual data
        'initial_investment': 10000,
        'max_drawdown': 10,
        'trades_executed': 5
    })
    
    # Generate the plot
    plot_filename = generate_stock_price_plot(actual_df, predicted_df)
    
    # Generate the PDF report
    pdf_filename = generate_pdf_report(metrics, plot_filename)
    
    # If the user wants a PDF report, return it
    if request.GET.get('format') == 'pdf':
        return FileResponse(open(pdf_filename, 'rb'), content_type='application/pdf')
    
    # Otherwise, return the report as JSON
    return JsonResponse({
        'status': 'success',
        'metrics': metrics,
        'predicted_prices': predicted_df.to_dict(orient='records')
    })