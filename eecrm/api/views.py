import logging
from datetime import datetime
from django.contrib.auth import get_user_model
from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import ValidationError

from .models import Client, Contract, Event
from .permissions import EmployeeRole
from .serializers import ClientSerializer, ContractSerializer, EventSerializer

import base.constants as cts

User = get_user_model()
logger = logging.getLogger(__name__)


class ClientViewSet(ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [EmployeeRole]


class ContractViewSet(ModelViewSet):
    serializer_class = ContractSerializer
    permission_classes = [EmployeeRole]

    def get_queryset(self):
        # filter the url shown to employees depending on action/method
        if self.request.method not in cts.READ_METHODS:

            client_id = self.kwargs.get("client_pk")
            contract_pk = self.kwargs.get("pk")
            if client_id and contract_pk:
                queryset = Contract.objects.filter(id=contract_pk)
            elif client_id:
                queryset = Contract.objects.filter(client_id=client_id)
            else:
                queryset = Contract.objects.all()
        return queryset

    def perform_create(self, serializer, *args, **kwargs):
        """body of target data to be created
        * create
            check user.department in ['S','M']
            check client url == client body
            check if user.department == 'S' alors sale_contact == request.user

        """
        create_data = self.request.data
        target_client_id = create_data["client"]
        target_sale_contact_id = create_data["sale_contact"]
        # current client in the url
        client_id = self.kwargs.get("clients_pk")
        connected_user_department = User.objects.filter(id=self.request.user.id).values('department')[0]["department"]
        # check user.department in ['S','M']
        # this is already checked thru permissions but we keep it in case we let thru to message
        if not connected_user_department in cts.SALES_ENABLED_DEPARTMENT:
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

        super().perform_create(serializer, *args, **kwargs)
        logger.info(f"{datetime.now()} : Contract.add {create_data}" f" by {request.user}")

    def perform_update(self, serializer, *args, **kwargs):
        """body of target data to be updated
            * perform_update 
            # status is to be set to true by Sales team 
            check user.department in ['S','M']
            check client url == client body
            check contract url == contract body
            check if user.department == 'S' alors sale_contact == request.user
            check payment_due change only if user.department == 'M'

        """
        update_data = self.request.data
        target_client_id = update_data["client"]
        target_contract_id = update_data["contract"]
        target_sale_contact_id = update_data["sale_contact"]
        target_payment_due = update_data["payment_due"]
        # current client in the url
        client_id = self.kwargs.get("clients_pk")
        contract_id = self.kwargs.get("pk")
        connected_user_department = User.objects.filter(id=self.request.user.id).values('department')[0]["department"]
        # check user.department in ['S','M']
        # this is already checked thru permissions but we keep it in case we let thru to message
        if not connected_user_department in cts.SALES_ENABLED_DEPARTMENT:
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
        before_payment_due = Contract.objects.get(pk=contract_id).payment_due
        if (connected_user_department != cts.USER_MANAGEMENT) and (target_payment_due != before_payment_due):
            error_message = f"""Dear {self.request.user} only managers are allowed to change payment due dates, pls check with the manager."""
            raise ValidationError(error_message)

        super().perform_update(serializer, *args, **kwargs)
        logger.info(f"{datetime.now()} : Contract.update {update_data}" f" by {request.user}")


class EventViewSet(ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [EmployeeRole]
