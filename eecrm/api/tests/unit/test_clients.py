import pytest

from api.models import Client
import base.constants as cts

class TestClients:

    @pytest.mark.django_db
    def test_create_client_instance(self):
        """Tests that we can retrieve an attribut of the just created client"""
        client = Client.objects.create(company_name=cts.TEST_COMPANY_NAME_1, sale_contact_id=1)
        assert client.__str__() == f"{cts.TEST_COMPANY_NAME_1} "

    @pytest.mark.django_db
    def test_delete_client_instance(self):
        """Tests that we can remove a client instance"""
        client = Client.objects.create(company_name=cts.TEST_COMPANY_NAME_1, sale_contact_id=1)
        number_of_client_in_db_before = Client.objects.count()
        client.delete()
        number_of_client_in_db_after = Client.objects.count()
        assert number_of_client_in_db_after + 1  == number_of_client_in_db_before