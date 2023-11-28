"""
Serializers for the items app.
"""
from rest_framework import serializers

from core.models import Item


class ItemSerializer(serializers.ModelSerializer):
    """Serializer for items."""

    class Meta:
        model = Item
        fields = ['id', 'name', 'price']
        read_only_fields = ['id']


class ItemDetailSerializer(ItemSerializer):
    """Serializer for item detail view."""

    class Meta(ItemSerializer.Meta):
        fields = ItemSerializer.Meta.fields + ['description']
