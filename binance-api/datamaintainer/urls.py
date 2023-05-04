from django.urls import path
from . import views

urlpatterns = [
    path('', views.fetch_data, name='data_update'),
    path('symbol/', views.update_symbol_list, name="symbol_update"),
    path('fetch/all/', views.fetch_all_available_data, name="fetch_all_available_data")
]