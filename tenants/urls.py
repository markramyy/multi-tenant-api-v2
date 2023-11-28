"""
URL mapping for tenants API
"""
from django.urls import path

from tenants import views


app_name = 'tenants'

urlpatterns = [
    path('create/', views.CreateTenantView.as_view(), name='create'),
    path('token/', views.CreateTokenView.as_view(), name='token'),
    path('me/', views.ManageTenantView.as_view(), name='me'),
]