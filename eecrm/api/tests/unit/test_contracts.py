import pytest
from django.contrib.auth import get_user_model
from api.models import Contract, Client
import base.constants as cts

User = get_user_model()


class TestContracts:

    @pytest.mark.django_db
    def test_create_contract_instance(self):
        """Tests that we can retrieve an attribut of the just created contract"""
        user = User.objects.create(username=cts.TEST_USERNAME_SALES,
                                   password=cts.TEST_SECRET_PASSWORD, department=cts.USER_SALES)
        client = Client.objects.create(username=cts.TEST_USERNAME_CLIENT, password=cts.TEST_SECRET_PASSWORD,
                                       company_name=cts.TEST_COMPANY_NAME_1, sale_contact_id=user.id)
        contract = Contract.objects.create(contract_name=cts.TEST_CONTRACT_NAME_1,
                                                  contract_amount=cts.TEST_CONTRACT_AMOUNT,
                                                  payment_due=cts.TEST_PAYMENT_DUE, client=client,
                                                  sale_contact=user)
        assert contract.__str__() == cts.TEST_CONTRACT_NAME_1

    @pytest.mark.django_db
    def test_delete_contract_instance(self):
        user = User.objects.create(username=cts.TEST_USERNAME_SALES,
                                   password=cts.TEST_SECRET_PASSWORD, department=cts.USER_SALES)
        client = Client.objects.create(username=cts.TEST_USERNAME_CLIENT, password=cts.TEST_SECRET_PASSWORD,
                                       company_name=cts.TEST_COMPANY_NAME_1, sale_contact_id=user.id)
        contract = Contract.objects.create(contract_name=cts.TEST_CONTRACT_NAME_1,
                                                  contract_amount=cts.TEST_CONTRACT_AMOUNT,
                                                  payment_due=cts.TEST_PAYMENT_DUE, client=client,
                                                  sale_contact=user)
        number_of_contract_in_db_before = Contract.objects.count()
        contract.delete()
        number_of_contract_in_db_after = Contract.objects.count()
        assert number_of_contract_in_db_after + 1 == number_of_contract_in_db_before
