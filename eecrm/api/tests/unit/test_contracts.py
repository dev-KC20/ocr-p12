import pytest

from api.models import Contract
import base.constants as cts

class TestContracts:

    @pytest.mark.django_db
    def test_create_contract_instance(self):
        """Tests that we can retrieve an attribut of the just created contract"""
        contract = Contract.objects.create(contract_name=cts.TEST_CONTRACT1)
        assert contract.__str__() == f"{cts.TEST_CONTRACT_NAME_1} "

    @pytest.mark.django_db
    def test_delete_contract_instance(self):
        """Tests that we can remove a contract instance"""
        contract = Contract.objects.create(company_name=cts.TEST_CONTRACT_NAME_1)
        number_of_contract_in_db_before = Contract.objects.count()
        contract.delete()
        number_of_contract_in_db_after = Contract.objects.count()
        assert number_of_contract_in_db_after + 1  == number_of_contract_in_db_before