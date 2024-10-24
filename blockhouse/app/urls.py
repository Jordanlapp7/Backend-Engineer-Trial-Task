from django.urls import path
from .views import fetch_data_view, backtest_view

urlpatterns = [
  path('fetch/<str:symbol>/', fetch_data_view, name='fetch_data'),
  path('backtest/<str:symbol>/<int:initial_investment>/', backtest_view, name='backtest'),
]