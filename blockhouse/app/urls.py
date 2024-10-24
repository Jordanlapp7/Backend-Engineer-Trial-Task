from django.urls import path
from .views import fetch_data_view

urlpatterns = [
  path('fetch/<str:symbol>/', fetch_data_view, name='fetch_data'),
]