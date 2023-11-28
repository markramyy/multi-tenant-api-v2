"""
Views for items APIs.
"""
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Item
from items import serializers


class ItemViewSet(viewsets.ModelViewSet):
    """Manage items in the database."""
    serializer_class = serializers.ItemDetailSerializer
    queryset = Item.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Return objects for the current authenticated tenant only."""
        return self.queryset.filter(tenant=self.request.user).order_by('-id')

    def get_serializer_class(self):
        """Return the serializer class for request."""
        if self.action == 'list':
            return serializers.ItemSerializer

        return self.serializer_class
