"""
Tests for the tenants models.
"""

from django.test import TestCase
from django.contrib.auth import get_user_model


class TestTenantsModels(TestCase):
    """Test the tenants models."""

    def test_create_tenant_with_email_successful(self):
        """Test creating a new tenant with a email is successful."""

        email = 'test@example.com'
        password = 'testpass123'
        tenant = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(tenant.email, email)
        self.assertTrue(tenant.check_password(password))
