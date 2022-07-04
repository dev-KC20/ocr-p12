from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Client


User = get_user_model()


class ApiAPITestCase(APITestCase):
    @classmethod
    def format_datetime(self, value):
        return value.strftime("%Y-%m-%dT%H:%M:%S.%fZ")


class TestClient(ApiAPITestCase):
    def setUp(self):
        email = "usertest@mail.fr"
        password = "password-oc"
        first_name = "johnny"
        last_name = "Cash"
        self.user = User.objects.create_user(
            email=email, password=password, first_name=first_name, last_name=last_name
        )

        jwt_fetch_data = {"email": email, "password": password}

        url = reverse("login")
        response = self.client.post(url, jwt_fetch_data, format="json")
        self.token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")

    def test_jwt_signup(self):

        url = reverse("signup")

        # signup user pass
        response = self.client.post(url, {"email": "usertest2@mail.fr", "password": "pass"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # signup same user fails
        response = self.client.post(url, {"email": "usertest2@mail.fr", "password": "pass"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_jwt_login(self):

        url = reverse("login")
        response = self.client.post(url, {"email": "usertest@mail.fr", "password": "password-oc"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue("access" in response.data)

    def test_jwt_bearer_credentials(self):

        verification_url = "/api/v1/Clients/"
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + "abc")
        response = self.client.get(verification_url, data={"format": "json"})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)
        response = self.client.get(verification_url, data={"format": "json"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_can_read_Client_list(self):
        url = reverse("Clients-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_can_create_Client(self):
        url = reverse("Clients-list")
        Client_number_before_create = Client.objects.count()
        data = {
            "title": "First Test Client",
            "description": " Long description of first test Client",
            "type": "B",
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        Client_number_after_create = Client.objects.count()
        self.assertEqual(Client_number_before_create + 1, Client_number_after_create)

    def test_put_can_update_Client(self):
        # create first to know existing pk to then update
        newly_created_Client = Client.objects.create(
            title="Second Test Client",
            description=" Long description of second test Client",
            type="F",
            author_user=self.user,
        )

        url = reverse("Clients-detail", kwargs=({"pk": newly_created_Client.pk}))
        # url = '/api/v1/Clients/1/'
        data = {
            "title": "Second Test Client updated",
            "description": " Long description of second updated test Client",
            "type": "B",
        }
        response = self.client.put(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
