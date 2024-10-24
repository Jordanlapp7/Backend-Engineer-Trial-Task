from django.urls import path
from .views import fetch_data_view, backtest_view, predict_stock_prices_api, generate_report

urlpatterns = [
  path('fetch/<str:symbol>/', fetch_data_view, name='fetch_data'),
  path('backtest/<str:symbol>/<int:initial_investment>/', backtest_view, name='backtest'),
  path('predict/<str:symbol>/', predict_stock_prices_api, name='predict_stock_prices_api'),
  path('report/<str:symbol>/', generate_report, name='generate_report'),
]