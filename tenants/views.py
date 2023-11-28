"""
Views for the tenant API.
"""
from rest_framework import generics

from tenants.serializers import TenantSerializer


class CreateTenantView(generics.CreateAPIView):
    """Create a new tenant in the system."""
    serializer_class = TenantSerializer
