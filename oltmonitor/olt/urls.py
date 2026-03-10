from django.urls import path
from .views import fetch_olt_onu

urlpatterns = [
    path('onus/', fetch_olt_onu),
]