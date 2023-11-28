"""
Test the item APIs.
"""
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Item

from items.serializers import ItemSerializer


ITEMS_URL = reverse('items:item-list')


def create_item(tenant, **params):
    """Create and return a sample item."""
    defaults = {
        'name': 'Sample Item',
        'price': Decimal('5.00'),
        'description': 'Sample description',
    }
    defaults.update(params)

    item = Item.objects.create(tenant=tenant, **defaults)
    return item


class PublicItemApiTests(TestCase):
    """Test Unauthenticated API requests."""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test that authentication is required."""
        res = self.client.get(ITEMS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateItemApiTests(TestCase):
    """Test authenticated API requests."""

    def setUp(self):
        self.client = APIClient()
        self.tenant = get_user_model().objects.create_user(
            'tenant@example.com',
            'testpass123',
        )
        self.client.force_authenticate(self.tenant)

    def test_retrieve_items(self):
        """Test retrieving a list of items."""
        create_item(tenant=self.tenant)
        create_item(tenant=self.tenant)

        res = self.client.get(ITEMS_URL)

        items = Item.objects.all().order_by('-id')
        serializer = ItemSerializer(items, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_items_limited_to_tenant(self):
        """Test list of items is limited to the authenticated tenant."""
        other_tenant = get_user_model().objects.create_user(
            'other@example.com',
            'password123',
        )
        create_item(tenant=other_tenant)
        create_item(tenant=self.tenant)

        res = self.client.get(ITEMS_URL)

        items = Item.objects.filter(tenant=self.tenant)
        serializer = ItemSerializer(items, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
