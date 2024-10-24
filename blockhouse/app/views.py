from django.http import JsonResponse
from .tasks import fetch_stock_data
from .backtest import generate_performance_summary

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