"""
URL mapping for tenants API
"""
from django.urls import path

from tenants import views


app_name = 'tenants'

urlpatterns = [
    path('create/', views.CreateTenantView.as_view(), name='create'),
]