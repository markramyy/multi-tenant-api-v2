"""
Serializers for the tenant API View.
"""
from django.contrib.auth import get_user_model

from rest_framework import serializers


class TenantSerializer(serializers.ModelSerializer):
    """Serializer for the tenant object."""

    class Meta:
        model = get_user_model()
        fields = ['email', 'password', 'name']
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    def create(self, validated_data):
        """Create and return a tenant with encrypted password."""
        return get_user_model().objects.create_tenant(**validated_data)
