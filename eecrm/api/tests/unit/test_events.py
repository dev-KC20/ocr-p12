import pytest
from django.contrib.auth import get_user_model
from api.models import Contract, Client, Event
import base.constants as cts

User = get_user_model()


class TestEvents:

    @pytest.mark.django_db
    def test_create_event_instance(self):
        """Tests that we can retrieve an attribut of the just created contract"""
        user = User.objects.create(username=cts.TEST_USERNAME_SALES,
                                   password=cts.TEST_SECRET_PASSWORD, department=cts.USER_SALES)
        user_support = User.objects.create(username=cts.TEST_USERNAME_SUPPORT,
                                           password=cts.TEST_SECRET_PASSWORD, department=cts.USER_SUPPORT)
        client = Client.objects.create(username=cts.TEST_USERNAME_CLIENT, password=cts.TEST_SECRET_PASSWORD,
                                       company_name=cts.TEST_COMPANY_NAME_1, sale_contact_id=user.id)
        contract = Contract.objects.create(contract_name=cts.TEST_CONTRACT_NAME_1,
                                           contract_amount=cts.TEST_CONTRACT_AMOUNT,
                                           payment_due=cts.TEST_PAYMENT_DUE, client=client,
                                           sale_contact=user)
        event = Event.objects.create(attendees=cts.TEST_EVENT_ATTENDEES,
                                     date_event=cts.TEST_PAYMENT_DUE, support_contact=user_support, contract=contract)
        assert event.get_event_attendees() == cts.TEST_EVENT_ATTENDEES

    @pytest.mark.django_db
    def test_delete_contract_instance(self):
        user = User.objects.create(username=cts.TEST_USERNAME_SALES,
                                   password=cts.TEST_SECRET_PASSWORD, department=cts.USER_SALES)
        user_support = User.objects.create(username=cts.TEST_USERNAME_SUPPORT,
                                           password=cts.TEST_SECRET_PASSWORD, department=cts.USER_SUPPORT)
        client = Client.objects.create(username=cts.TEST_USERNAME_CLIENT, password=cts.TEST_SECRET_PASSWORD,
                                       company_name=cts.TEST_COMPANY_NAME_1, sale_contact_id=user.id)
        contract = Contract.objects.create(contract_name=cts.TEST_CONTRACT_NAME_1,
                                           contract_amount=cts.TEST_CONTRACT_AMOUNT,
                                           payment_due=cts.TEST_PAYMENT_DUE, client=client,
                                           sale_contact=user)
        event = Event.objects.create(attendees=cts.TEST_EVENT_ATTENDEES,
                                     date_event=cts.TEST_PAYMENT_DUE, support_contact=user_support, contract=contract)
        number_of_event_in_db_before = Event.objects.count()
        event.delete()
        number_of_event_in_db_after = Event.objects.count()
        assert number_of_event_in_db_after + 1 == number_of_event_in_db_before
