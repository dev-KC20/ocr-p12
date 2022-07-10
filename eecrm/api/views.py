# import the logging library
import logging
from datetime import datetime
from django.contrib.auth import get_user_model
from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import ValidationError

from .filters import ContractFilter
from .models import Client, Contract, Event
from .permissions import HasManagerRole, HasSupportRole, HasSalesRole
from .serializers import ClientSerializer, ContractSerializer, EventSerializer

import base.constants as cts

User = get_user_model()
logger = logging.getLogger(__name__)
logger.info(cts.HELLO_WORLD)


def get_data_or_error(request_data, field_name, get_data):
    if field_name not in request_data:
        error_message = f""" {field_name} is missing in the body of the request, pls complete it. """
        raise ValidationError(error_message)
    else:
        if get_data:
            return request_data[field_name]
        else:
            return None


class ClientViewSet(ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [HasManagerRole, HasSalesRole]


class ContractViewSet(ModelViewSet):
    serializer_class = ContractSerializer
    permission_classes = [HasManagerRole, HasSalesRole]
    filterset_class = ContractFilter
    search_fields = ["contract_name"]
    ordering_fields = ["contract_name"]

    def get_queryset(self):
        # filter the url shown to employees depending on action/method
        # self.action == 'list'
        # if self.request.method not in cts.READ_METHODS:

        client_id = self.kwargs.get("clients_pk")
        contract_pk = self.kwargs.get("pk")
        if client_id and contract_pk:
            self.queryset = Contract.objects.filter(id=contract_pk)
        elif client_id:
            self.queryset = Contract.objects.filter(client_id=client_id)
        else:
            self.queryset = Contract.objects.all()
        return self.queryset

    def perform_create(self, serializer, *args, **kwargs):
        """body of target data to be created
        * create
            check user.department in ['S','M']
            check client url == client body
            check client is not prospect
            check if user.department == 'S' alors sale_contact == request.user

        """
        # check for mandatory fields in body of request
        get_data_or_error(self.request.data, "contract_name", False)
        get_data_or_error(self.request.data, "contract_amount", False)
        get_data_or_error(self.request.data, "payment_due", False)
        target_client_id = get_data_or_error(self.request.data, "client", True)
        target_sale_contact_id = get_data_or_error(self.request.data, "sale_contact", True)

        # check url & get current client
        client_id = self.kwargs.get("clients_pk")
        connected_user_department = User.objects.filter(id=self.request.user.id).values("department")[0]["department"]
        # check user.department in ['S','M']
        # this is already checked thru permissions but we keep it in case we let thru to message
        if connected_user_department not in cts.SALES_ENABLED_DEPARTMENT:
            error_message = f"""You, user {self.request.user}
             need to be member of Sales, pls work on this with the sales team."""
            raise ValidationError(error_message)

        # owasp : do not temper with client in the data
        if not (int(client_id) == int(target_client_id)):
            error_message = f"""you are not allowed to change the client {target_client_id},
             pls go back and select: {client_id}"""
            raise ValidationError(error_message)
        # check if user.department == 'S' alors sale_contact == request.user
        if (connected_user_department == cts.USER_SALES) and (target_sale_contact_id != self.request.user.id):
            error_message = f"""You {self.request.user} are the sales contact, pls put your user id as contact."""
            raise ValidationError(error_message)
        # check client is not prospect
        target_client = Client.objects.get(id=target_client_id)
        if target_client.is_prospect:
            error_message = (
                f"""This client is still a prospect. Please upgrade him full client before adding contract."""
            )
            raise ValidationError(error_message)
        super().perform_create(serializer, *args, **kwargs)
        logger.info(f"[{datetime.now()}]: Contract.add {self.request.data} by {self.request.user}")

    def perform_update(self, serializer, *args, **kwargs):
        """body of target data to be updated
        * perform_update
        check that status is to be set to true by Sales team
        check user.department in ['S','M']
        check client url == client body
        check contract url == contract body
        check if user.department == 'S' alors sale_contact == request.user
        check payment_due change only if user.department == 'M'

        """
        # check for mandatory fields in body of request
        target_status = get_data_or_error(self.request.data, "status", True)
        get_data_or_error(self.request.data, "contract_name", False)
        get_data_or_error(self.request.data, "contract_amount", False)
        target_payment_due_str = get_data_or_error(self.request.data, "payment_due", True)

        target_sale_contact_id = get_data_or_error(self.request.data, "sale_contact", True)
        target_client_id = get_data_or_error(self.request.data, "client", True)
        target_contract_id = get_data_or_error(self.request.data, "id", True)
        # check url & get current client & contract
        client_id = self.kwargs.get("clients_pk")
        contract_id = self.kwargs.get("pk")

        connected_user_department = User.objects.filter(id=self.request.user.id).values("department")[0]["department"]
        # check user.department in ['S','M']
        # this is already checked thru permissions but we keep it in case we let thru to message
        if connected_user_department not in cts.SALES_ENABLED_DEPARTMENT:
            error_message = f"""You, user {self.request.user}
             need to be member of Sales, pls work on this with the sales team."""
            raise ValidationError(error_message)
        # owasp : do not temper with client in the data
        if not (int(client_id) == int(target_client_id)):
            error_message = f"""you are not allowed to change the client {target_client_id},
             pls go back and select: {client_id}"""
            raise ValidationError(error_message)
        # owasp : do not temper with contract in the data
        if not (int(contract_id) == int(target_contract_id)):
            error_message = f"""you are not allowed to change the contract {target_contract_id},
             pls go back and select: {contract_id}"""
            raise ValidationError(error_message)
        # check if user.department == 'S' alors sale_contact == request.user
        if (connected_user_department == cts.USER_SALES) and (target_sale_contact_id != self.request.user.id):
            error_message = f"""You {self.request.user} are the sales contact, pls put your user id as contact."""
            raise ValidationError(error_message)
        # check payment_due change only if user.department == 'M'
        before_contract = Contract.objects.get(pk=contract_id)
        before_status = before_contract.status
        # no payment due in body if not manager
        if (connected_user_department != cts.USER_MANAGEMENT) and (target_payment_due_str):
            error_message = f"""Dear {self.request.user} only managers are 
                allowed to change payment due dates, pls check with the manager."""
            raise ValidationError(error_message)
        # check that status is changed only by Sales team (& Management)
        # this is already checked as only sale can change contracts but we keep it in case we let thru to message
        if connected_user_department not in cts.SALES_ENABLED_DEPARTMENT and before_status != target_status:
            error_message = """Only a sales member team is allowed to change the status, pls check with Sales."""
            raise ValidationError(error_message)
        super().perform_update(serializer, *args, **kwargs)
        logger.info(f"[{datetime.now()}]: Contract.update {self.request.data} by {self.request.user}")


class EventViewSet(ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [HasManagerRole, HasSalesRole, HasSupportRole]
