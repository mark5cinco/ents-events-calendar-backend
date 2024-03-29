from django.test import TestCase

# Create your tests here.
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from accounts.models import User


class ModelTestCase(TestCase):
    """This class defines the test suite for the User model."""

    def setUp(self):
        """Define the test client and other test variables."""
        self.email = "user@test.com"
        self.User = User(email=self.email)

    def test_model_can_create_a_user(self):
        """Test the User model can create a User."""
        old_count = User.objects.count()
        self.User.save()
        new_count = User.objects.count()
        self.assertNotEqual(old_count, new_count)


class ViewTestCase(TestCase):
    """Test suite for the api views."""

    def setUp(self):
        """Define the test client and other test variables."""
        self.client = APIClient()
        self.user_data = {
            'email': 'user@test.com',
            'password': 'test',
            'profile': {
                'gender': 'm',
                'birthday': '1992-01-01'
            }
        }
        self.response = self.client.post(
            reverse('create'),
            self.user_data,
            format="json"
        )

    def test_api_can_create_a_user(self):
        """Test the api has bucket creation capability."""
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)

    def test_api_can_get_a_user(self):
        """Test the api can get a given user."""
        user = User.objects.get()
        response = self.client.get(
            reverse('details', kwargs={'pk': user.id}),
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, user)

    def test_api_can_update_user(self):
        """Test the api can update a given user."""
        user = User.objects.get()
        change_user = {'first_name': 'Something new'}
        res = self.client.patch(
            reverse('details', kwargs={'pk': user.id}),
            change_user,
            format='json'
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_api_can_delete_user(self):
        """Test the api can delete a user."""
        user = User.objects.get()
        response = self.client.delete(
            reverse('details', kwargs={'pk': user.id}),
            format='json',
            follow=True
        )

        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)
