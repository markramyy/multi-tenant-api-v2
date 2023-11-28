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

from items.serializers import ItemSerializer, ItemDetailSerializer


ITEMS_URL = reverse('items:item-list')


def detail_url(item_id):
    """Return item detail URL."""
    return reverse('items:item-detail', args=[item_id])


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


def create_tenant(**params):
    """Create and return a new tenant."""
    return get_user_model().objects.create_user(**params)


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
        self.tenant = create_tenant(email='tenant@example.com', password='test123')
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
        other_tenant = create_tenant(email='other@example.com', password='password123')
        create_item(tenant=other_tenant)
        create_item(tenant=self.tenant)

        res = self.client.get(ITEMS_URL)

        items = Item.objects.filter(tenant=self.tenant)
        serializer = ItemSerializer(items, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_get_item_detail(self):
        """Test viewing an item detail."""
        item = create_item(tenant=self.tenant)

        url = detail_url(item.id)
        res = self.client.get(url)

        serializer = ItemDetailSerializer(item)
        self.assertEqual(res.data, serializer.data)

    def test_create_item(self):
        """Test creating an item."""
        payload = {
            'name': 'Sample Item',
            'price': Decimal('5.00'),
            'description': 'Sample description',
        }
        res = self.client.post(ITEMS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        item = Item.objects.get(id=res.data['id']) # retrieve the item from the database
        for key in payload.keys():
            self.assertEqual(payload[key], getattr(item, key)) # retrieve the value of the attribute
        self.assertEqual(item.tenant, self.tenant)

    def test_partial_update_item(self):
        """Test updating an item with patch."""
        original_price = Decimal('5.00')
        item = create_item(tenant=self.tenant, name='Item Name', price=original_price)

        payload = {'name': 'New Item Name'}
        url = detail_url(item.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        item.refresh_from_db()
        self.assertEqual(item.name, payload['name'])
        self.assertEqual(item.price, original_price)
        self.assertEqual(item.tenant, self.tenant)

    def test_full_update_item(self):
        """Test updating an item with put."""
        item = create_item(
            tenant=self.tenant,
            name='Item Name',
            price=Decimal('5.00'),
            description='Sample description',
        )

        payload = {
            'name': 'New Item Name',
            'price': Decimal('10.00'),
            'description': 'New description',
        }
        url = detail_url(item.id)
        res = self.client.put(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        item.refresh_from_db()
        for key in payload.keys():
            self.assertEqual(payload[key], getattr(item, key))
        self.assertEqual(item.tenant, self.tenant)

    def test_update_tenant_returns_error(self):
        """Test changing the item tenant results in an error."""
        new_tenant = create_tenant(email='tenant2@example.com', password='password123')
        item = create_item(tenant=self.tenant)

        payload = {'tenant': new_tenant.id}
        url = detail_url(item.id)
        self.client.patch(url, payload)

        item.refresh_from_db()
        self.assertEqual(item.tenant, self.tenant)
