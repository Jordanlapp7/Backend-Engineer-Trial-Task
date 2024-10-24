from django.http import JsonResponse
from .tasks import fetch_stock_data

def fetch_data_view(request, symbol):
    try:
        fetch_stock_data(symbol)
        return JsonResponse({"status": "success", "message": f"Data for {symbol} fetched successfully."})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})