from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .models import Item
from django.contrib.auth import get_user_model

User = get_user_model()


class ItemTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        login_success = self.client.login(username='testuser', password='testpassword')
        self.assertTrue(login_success, "User login failed")  # Check if login was successful
        self.item_data = {'name': 'Test Item', 'description': 'Test Description', 'quantity': 10.0}

    def test_create_item(self):
        url = reverse('create_item')
        response = self.client.post(url, self.item_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], self.item_data['name'])

    def test_create_item_already_exists(self):
        Item.objects.create(name='Test Item', description='Test Description', quantity=10.0)
        url = reverse('create_item')
        response = self.client.post(url, self.item_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Item already exists.')

    def test_read_item(self):
        item = Item.objects.create(name='Test Item', description='Test Description', quantity=10.0)
        url = reverse('read_item', args=[item.id])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], item.name)

    def test_read_item_not_found(self):
        url = reverse('read_item', args=[999])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['error'], 'Item not found.')

    def test_update_item(self):
        item = Item.objects.create(name='Test Item', description='Test Description', quantity=10.0)
        updated_data = {'name': 'Updated Item', 'description': 'Updated Description', 'quantity': 20.0}
        url = reverse('update_item', args=[item.id])
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], updated_data['name'])

    def test_update_item_not_found(self):
        updated_data = {'name': 'Updated Item', 'description': 'Updated Description', 'quantity': 20.0}
        url = reverse('update_item', args=[999])
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['error'], 'Item not found.')

    def test_delete_item(self):
        item = Item.objects.create(name='Test Item', description='Test Description', quantity=10.0)
        url = reverse('delete_item', args=[item.id])
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['success'], 'Item deleted.')

    def test_delete_item_not_found(self):
        url = reverse('delete_item', args=[999])
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['error'], 'Item not found.')