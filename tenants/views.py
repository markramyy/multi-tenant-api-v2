"""
Views for the tenant API.
"""
from rest_framework import generics, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from tenants.serializers import TenantSerializer, AuthTokenSerializer


class CreateTenantView(generics.CreateAPIView):
    """Create a new tenant in the system."""
    serializer_class = TenantSerializer


class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for the tenant."""
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

class ManageTenantView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated tenant."""
    serializer_class = TenantSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """Retrieve and return the authenticated tenant."""
        return self.request.user
