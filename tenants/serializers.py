"""
Serializers for the tenant API View.
"""
from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import gettext as _
from rest_framework import serializers


class TenantSerializer(serializers.ModelSerializer):
    """Serializer for the tenant object."""

    class Meta:
        model = get_user_model()
        fields = ['email', 'password', 'name']
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    def create(self, validated_data):
        """Create and return a tenant with encrypted password."""
        return get_user_model().objects.create_user(**validated_data)


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the tenant auth token."""
    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False,
    )

    def validate(self, attrs):
        """Validate and authenticate the tenant."""
        email = attrs.get('email')
        password = attrs.get('password')
        tenant = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password,
        )
        if not tenant:
            msg = _('Unable to authenticate with provided credentials.')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['tenant'] = tenant
        return attrs
