import pytest

# from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User
import base.constants as cts

from api.models import Client

# User = get_user_model()


class ApiAPITestCase(APITestCase):
    @classmethod
    def format_datetime(self, value):
        return value.strftime("%Y-%m-%dT%H:%M:%S.%fZ")


class TestUserAuthenticate(APITestCase):
    @pytest.mark.django_db
    def setUp(self):

        self.username = cts.TEST_USERNAME_MANAGEMENT
        self.password = cts.TEST_SECRET_PASSWORD
        self.department = cts.USER_MANAGEMENT

        self.user = User.objects.create_user(
            username=self.username,
            password=self.password,
            department=self.department,
        )
        self.user.is_active
        self.user.is_staff
        self.user.save()
        self.client.login(
            username=self.username,
            password=self.password,
        )

        jwt_fetch_data = {"username": self.username, "password": self.password}

        url = reverse("login")
        response = self.client.post(url, jwt_fetch_data, format="json")
        self.token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")

    @pytest.mark.django_db
    def test_can_log_with_jwt_token(self):
        """
        GIVEN a Django application configured for testing
        WHEN the '/login' page is requested (POST)
        THEN check that the response is valid & user gets an access token
        """
        jwt_fetch_data = {"username": self.username, "password": self.password}

        url = reverse("login")
        response = self.client.post(url, jwt_fetch_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue("access" in response.data)
    
    @pytest.mark.django_db
    def test_use_of_jwt_bearer_credentials(self):
        verification_url = reverse("clients-list")
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + "abc")
        response = self.client.get(verification_url, data={"format": "json"})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)
        response = self.client.get(verification_url, data={"format": "json"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @pytest.mark.django_db
    def test_can_read_contracts_details(self):
        # create a customer
        customer = Client.objects.create(company_name=cts.TEST_COMPANY_NAME_1, sale_contact_id=1)
        verification_url = reverse("clients-detail", args=([customer.id]))
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)
        response = self.client.get(verification_url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)



