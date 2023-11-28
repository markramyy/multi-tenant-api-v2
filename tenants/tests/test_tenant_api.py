"""
Tests for the tenant API.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


CREATE_TENANT_URL = reverse('tenants:create')
TOKEN_URL = reverse('tenants:token')
ME_URL = reverse('tenants:me')


def create_tenant(**params):
    """Create and return a new tenant."""
    return get_user_model().objects.create_user(**params)


class PublicTenantApiTests(TestCase):
    """Test the public feautures of the tenant API."""

    def setUp(self):
        self.client = APIClient()

    def test_create_tenant_success(self):
        """Test creating a tenant is successful."""
        payload = {
            'email': 'test@example.com',
            'password': 'testpass123',
            'name': 'Test Name',
        }
        res = self.client.post(CREATE_TENANT_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        tenant = get_user_model().objects.get(email=payload['email'])
        self.assertTrue(tenant.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_tenant_with_email_exists(self):
        """Test creating a tenant that already exists fails."""
        payload = {
            'email': 'test@example.com',
            'password': 'testpass123',
            'name': 'Test Name',
        }
        create_tenant(**payload)
        res = self.client.post(CREATE_TENANT_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short_error(self):
        """Test that the password must be more than 8 characters."""
        payload = {
            'email': 'test@example.com',
            'password': 'pw',
            'name': 'Test Name',
        }
        res = self.client.post(CREATE_TENANT_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        tenant_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(tenant_exists)

    def test_create_token_for_user(self):
        """Test generates token for valid credentials."""
        user_details = {
            'name': 'Test Name',
            'email': 'test@example.com',
            'password': 'test-user-password123',
        }
        create_tenant(**user_details)

        payload = {
            'email': user_details['email'],
            'password': user_details['password'],
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_bad_credentials(self):
        """Test returns error if credentials invalid."""
        create_tenant(email='test@example.com', password='goodpass')

        payload = {'email': 'test@example.com', 'password': 'badpass'}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_blank_password(self):
        """Test posting a blank password returns an error."""
        payload = {'email': 'test@example.com', 'password': ''}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_user_unauthorized(self):
        """Test authentication is required for users."""
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTenantApiTests(TestCase):
    """Test API requests that require authentication."""

    def setUp(self):
        self.tenant = create_tenant(
            email='test@example.com',
            password='testpass123',
            name='Test Name',
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_profile_success(self):
        """Test retrieving profile for logged in tenant."""
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {
            'name': self.tenant.name,
            'email': self.tenant.email,
        })

    def test_post_me_not_allowed(self):
        """Test that POST is not allowed on the me endpoint."""
        res = self.client.post(ME_URL, {})

        self.assertEqual(
            res.status_code,
            status.HTTP_405_METHOD_NOT_ALLOWED,
        )

    def test_update_tenant_profile(self):
        """Test updating the tenant profile for authenticated user."""
        payload = {'name': 'New Name', 'password': 'newpass123'}

        res = self.client.patch(ME_URL, payload)

        self.tenant.refresh_from_db()
        self.assertEqual(self.tenant.name, payload['name'])
        self.assertTrue(self.tenant.check_password(payload['password']))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
