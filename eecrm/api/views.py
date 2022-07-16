# import the logging library
import logging
from datetime import datetime
from django.contrib.auth import get_user_model
from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import ValidationError

from .filters import ContractFilter
from .models import Client, Contract, Event
from .permissions import HasSupportRole, HasSalesRole
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
    permission_classes = [HasSalesRole]

    def get_queryset(self):
        # filter the url shown to employees depending on action/method
        # self.action == 'list'
        client_pk = self.kwargs.get("pk")
        connected_user_department = User.objects.filter(id=self.request.user.id).values(
            "department"
        )[0]["department"]
        if connected_user_department != cts.USER_EXTERNAL:
            if not (client_pk is None or client_pk == "null"):
                self.queryset = Client.objects.filter(id=client_pk)
            else:
                self.queryset = Client.objects.all()
        else:
            # client is an external user
            self.queryset = Client.objects.filter(id=self.request.user.id)
        return self.queryset

    def perform_create(self, serializer, *args, **kwargs):
        """body of target data to be created
        * create
            check client username is provided
            check user.department in ['S','M']
            check if user.department == 'S' alors sale_contact == request.user

        """
        # check for mandatory fields in body of request
        get_data_or_error(self.request.data, "company_name", False)
        target_client_username = get_data_or_error(self.request.data, "username", True)
        target_client_password = get_data_or_error(self.request.data, "password", True)
        target_sale_contact_id = get_data_or_error(
            self.request.data, "sale_contact", True
        )

        connected_user_department = User.objects.filter(id=self.request.user.id).values(
            "department"
        )[0]["department"]
        # check user.department in ['S','M']
        # this is already checked thru permissions but we keep it in case we let thru to message
        if connected_user_department not in cts.SALES_ENABLED_DEPARTMENT:
            error_message = f"""You, user {self.request.user}
                need to be member of Sales, pls work on this with the sales team."""
            raise ValidationError(error_message)

        # provide username and password for clients
        if not (target_client_username) or not (target_client_password):
            error_message = """username and password are mandatory for the client,
                pls provide some."""
            raise ValidationError(error_message)
        # check if username for clients does not exists
        target_client = Client.objects.filter(username=target_client_username)
        target_user_client = User.objects.filter(username=target_client_username)
        if target_client.exists() or target_user_client.exists():
            error_message = f""" Sorry the {target_client_username} username is already taken,
                pls provide select another."""
            raise ValidationError(error_message)
        # check if user.department == 'S' alors sale_contact == request.user
        if (connected_user_department == cts.USER_SALES) and (
            target_sale_contact_id != self.request.user.id
        ):
            error_message = f"""You {self.request.user} are the sales contact, pls put your user id as contact."""
            raise ValidationError(error_message)

        super().perform_create(serializer, *args, **kwargs)
        cleaned_request_data = self.request.data
        if cleaned_request_data["password"]:
            cleaned_request_data["password"] = ""
        logger.info(
            f"[{datetime.now()}]: Client.add {cleaned_request_data} by {self.request.user}"
        )

    def perform_update(self, serializer, *args, **kwargs):
        """body of target data to be created
        * create
            check url contains client id
            check if client id in url == in body
            check client username shall not be provided, nor password
            check user.department in ['S','M']
            check if user.department == 'S' alors sale_contact == request.user

        """

        # check for mandatory fields in body of request
        get_data_or_error(self.request.data, "company_name", False)
        target_client_id = get_data_or_error(self.request.data, "id", True)
        get_data_or_error(self.request.data, "username", False)
        get_data_or_error(self.request.data, "password", False)
        target_sale_contact_id = get_data_or_error(
            self.request.data, "sale_contact", True
        )
        get_data_or_error(self.request.data, "is_prospect", False)

        connected_user_department = User.objects.filter(id=self.request.user.id).values(
            "department"
        )[0]["department"]

        # check url & get current client
        client_pk = self.kwargs.get("pk")
        if client_pk is None or client_pk == "null":
            error_message = """The url has been messed up, please try again."""
            raise ValidationError(error_message)
        # owasp : do not temper with client in the data/url
        if target_client_id:
            if int(client_pk) != int(target_client_id):
                error_message = f"""you are not allowed to change the client {target_client_id},
                pls go back and select: {client_pk}"""
                raise ValidationError(error_message)

        # check user.department in ['S','M']
        # this is already checked thru permissions but we keep it in case we let thru to message
        if connected_user_department not in cts.SALES_ENABLED_DEPARTMENT:
            error_message = f"""You, user {self.request.user}
                need to be member of Sales, pls work on this with the sales team."""
            raise ValidationError(error_message)

        # # do not change username and password for clients but in Admin
        # if (target_client_username) or (target_client_password):
        #     error_message = f"""username or password shall not be modiifed here,
        #         pls check with manager."""
        #     raise ValidationError(error_message)
        # check if user.department == 'S' alors sale_contact == request.user
        if (connected_user_department == cts.USER_SALES) and (
            target_sale_contact_id != self.request.user.id
        ):
            error_message = f"""You {self.request.user} are the sales contact, pls put your user id as contact."""
            raise ValidationError(error_message)

        super().perform_create(serializer, *args, **kwargs)
        logger.info(
            f"[{datetime.now()}]: Client.update {self.request.data} by {self.request.user}"
        )


class ContractViewSet(ModelViewSet):
    serializer_class = ContractSerializer
    permission_classes = [HasSalesRole]
    filterset_class = ContractFilter
    search_fields = ["contract_name"]
    ordering_fields = ["contract_name"]

    def get_queryset(self):
        # filter the url shown to employees depending on action/method
        # self.action == 'list'
        # if self.request.method not in cts.READ_METHODS:

        # check url client
        client_pk = self.kwargs.get(
            "clients_pk"
        )  # client_pk when models Contract/Events
        if client_pk is None or client_pk == "null":
            error_message = """The url has been messed up, please try again."""
            raise ValidationError(error_message)
        # check url contract
        contract_pk = self.kwargs.get("pk")
        if contract_pk:
            if contract_pk is None or contract_pk == "null":
                error_message = """The url has been messed up, please try again."""
                raise ValidationError(error_message)

        if client_pk and contract_pk:
            self.queryset = Contract.objects.filter(id=contract_pk)
        elif client_pk:
            self.queryset = Contract.objects.filter(client_id=client_pk)
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
        target_sale_contact_id = get_data_or_error(
            self.request.data, "sale_contact", True
        )
        # who is the connected user
        connected_user_department = User.objects.filter(id=self.request.user.id).values(
            "department"
        )[0]["department"]
        # check url & get current client
        client_id = self.kwargs.get("clients_pk")
        # this is already checked thru permissions but we keep it in case we let thru to message
        if client_id is None or client_id == "null":
            error_message = """The url has been messed up, please try again."""
            raise ValidationError(error_message)
        # owasp : do not temper with client in the data
        if int(client_id) != int(target_client_id):
            error_message = f"""you are not allowed to change the client {target_client_id},
             pls go back and select: {client_id}"""
            raise ValidationError(error_message)
        # check user.department in ['S','M']
        # this is already checked thru permissions but we keep it in case we let thru to message
        if connected_user_department not in cts.SALES_ENABLED_DEPARTMENT:
            error_message = f"""You, user {self.request.user}
             need to be member of Sales, pls work on this with the sales team."""
            raise ValidationError(error_message)

        # check if user.department == 'S' alors sale_contact == request.user
        if (connected_user_department == cts.USER_SALES) and (
            target_sale_contact_id != self.request.user.id
        ):
            error_message = f"""You {self.request.user} are the sales contact, pls put your user id as contact."""
            raise ValidationError(error_message)
        # check client is not prospect
        target_client = Client.objects.get(id=target_client_id)
        if target_client.is_prospect:
            error_message = """This client is still a prospect.
            Please upgrade him full client before adding contract."""
            raise ValidationError(error_message)
        super().perform_create(serializer, *args, **kwargs)
        logger.info(
            f"[{datetime.now()}]: Contract.add {self.request.data} by {self.request.user}"
        )

    def perform_update(self, serializer, *args, **kwargs):
        """body of target data to be updated
        * perform_update
        check that status is to be set to true by Sales team
        check user.department in ['S','M']
        check client url == client body
        check contract url == contract body
        check if user.department == 'S' alors sale_contact == request.user
        ** canceled** check payment_due change only if user.department == 'M'

        """
        # check for mandatory fields in body of request
        target_status = get_data_or_error(self.request.data, "status", True)
        get_data_or_error(self.request.data, "contract_name", False)
        get_data_or_error(self.request.data, "contract_amount", False)
        get_data_or_error(self.request.data, "payment_due", False)

        target_sale_contact_id = get_data_or_error(
            self.request.data, "sale_contact", True
        )
        target_client_id = get_data_or_error(self.request.data, "client", True)
        target_contract_id = get_data_or_error(self.request.data, "id", True)
        # check url & get current client & contract
        client_id = self.kwargs.get("clients_pk")
        contract_id = self.kwargs.get("pk")

        connected_user_department = User.objects.filter(id=self.request.user.id).values(
            "department"
        )[0]["department"]
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
        if (connected_user_department == cts.USER_SALES) and (
            target_sale_contact_id != self.request.user.id
        ):
            error_message = f"""You {self.request.user} are the sales contact, pls put your user id as contact."""
            raise ValidationError(error_message)
        # check payment_due change only if user.department == 'M'
        before_contract = Contract.objects.get(pk=contract_id)
        before_status = before_contract.status
        # # no payment due in body if not manager
        # if (connected_user_department != cts.USER_MANAGEMENT) and (
        #     target_payment_due_str
        # ):
        #     error_message = f"""Dear {self.request.user} only managers are
        #         allowed to change payment due dates, pls check with the manager."""
        #     raise ValidationError(error_message)
        # check that status is changed only by Sales team (& Management)
        # this is already checked as only sale can change contracts but we keep it in case we let thru to message
        if (
            connected_user_department not in cts.SALES_ENABLED_DEPARTMENT
            and before_status != target_status
        ):
            error_message = """Only a sales member team is allowed to change the status, pls check with Sales."""
            raise ValidationError(error_message)
        super().perform_update(serializer, *args, **kwargs)
        logger.info(
            f"[{datetime.now()}]: Contract.update {self.request.data} by {self.request.user}"
        )


class EventViewSet(ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    # permission_classes = [HasSalesRole, HasSupportRole]
    permission_classes = [HasSalesRole, HasSupportRole]

    def get_queryset(self):
        # check url client
        client_pk = self.kwargs.get(
            "clients_pk"
        )  # client_pk when models Contract/Events
        if client_pk is None or client_pk == "null":
            error_message = (
                """The client part of url has been messed up, please try again."""
            )
            raise ValidationError(error_message)
        # check url contract
        contract_pk = self.kwargs.get("contracts_pk")
        if contract_pk:
            if contract_pk is None or contract_pk == "null":
                error_message = (
                    """The contract part of url has been messed up, please try again."""
                )
                raise ValidationError(error_message)
        # check url event
        event_pk = self.kwargs.get("pk")
        if event_pk:
            if event_pk is None or event_pk == "null":
                error_message = (
                    """The event part of url has been messed up, please try again."""
                )
                raise ValidationError(error_message)

        if client_pk and contract_pk and event_pk:
            self.queryset = Event.objects.filter(id=event_pk)
        elif contract_pk:
            self.queryset = Event.objects.filter(contract_id=contract_pk)
        else:
            self.queryset = Event.objects.all()
        return self.queryset

    def perform_create(self, serializer, *args, **kwargs):
        """body of target data to be created
        fields = ["event_status","attendees","date_event","notes","date_created",
                   "date_updated","support_contact","contract",]
        * create
            check user.department in ['S','M']
            check client url == client body
            check contract url == contract body
            check event_status is Open
            check support_contact is mandatory & department = 'A'


        """

        # check url client
        client_pk = self.kwargs.get(
            "clients_pk"
        )  # client_pk when models Contract/Events
        if client_pk is None or client_pk == "null":
            error_message = (
                """The client part of url has been messed up, please try again."""
            )
            raise ValidationError(error_message)
        # check url contract
        contract_pk = self.kwargs.get("contracts_pk")
        if contract_pk:
            if contract_pk is None or contract_pk == "null":
                error_message = (
                    """The contract part of url has been messed up, please try again."""
                )
                raise ValidationError(error_message)
        # check url event

        # check for mandatory fields in body of request
        target_event_status = get_data_or_error(self.request.data, "event_status", True)
        get_data_or_error(self.request.data, "attendees", False)
        get_data_or_error(self.request.data, "date_event", False)
        target_support_contact_id = get_data_or_error(
            self.request.data, "support_contact", True
        )
        target_contract = get_data_or_error(self.request.data, "contract", True)

        connected_user_department = User.objects.filter(id=self.request.user.id).values(
            "department"
        )[0]["department"]
        # check user.department in ['S','M']
        # this is already checked thru permissions but we keep it in case we let thru to message

        if connected_user_department not in cts.SALES_ENABLED_DEPARTMENT:
            error_message = f"""You, user {self.request.user}
             need to be member of Sales, pls work on this with the sales team."""
            raise ValidationError(error_message)

        # owasp : do not temper with contract in the data
        if int(contract_pk) != target_contract:
            error_message = f"""you are not allowed to change the contract {target_contract},
             pls go back and select: {contract_pk}"""
            raise ValidationError(error_message)
        # check event_status is Open
        if target_event_status != cts.EVENT_OPEN:
            error_message = f"""When creating an event, the satus can only be {cts.EVENT_OPEN},
             pls correct."""
            raise ValidationError(error_message)
        # check support_contact mandatory
        if not (target_support_contact_id):
            error_message = f"""You {self.request.user} shall allocate a support contact, pls retry."""
            raise ValidationError(error_message)
        # check support_contact is mandatory & department = 'A'
        contact_user_department = User.objects.filter(
            id=target_support_contact_id
        ).values("department")[0]["department"]
        if contact_user_department not in cts.SUPPORT_ENABLED_DEPARTMENT:
            error_message = """The support contact shall belong to the support department, pls retry."""
            raise ValidationError(error_message)

        super().perform_create(serializer, *args, **kwargs)
        logger.info(
            f"[{datetime.now()}]: Event.add {self.request.data} by {self.request.user}"
        )

    def perform_update(self, serializer, *args, **kwargs):
        """body of target data to be created
        fields = ["event_status","attendees","date_event","notes","date_created",
                   "date_updated","support_contact","contract",]
        * update
            check user.department in ['A']
            check client url == client body
            check contract url == contract body
            check event_status is present


        """
        # check for mandatory fields in body of request
        target_event_status = get_data_or_error(
            self.request.data, "event_status", False
        )
        get_data_or_error(self.request.data, "attendees", False)
        get_data_or_error(self.request.data, "date_event", False)
        target_support_contact_id = get_data_or_error(
            self.request.data, "support_contact", True
        )
        target_contract = get_data_or_error(self.request.data, "contract", True)

        # check url & get current client
        # client_pk = self.kwargs.get("clients_pk")
        contract_pk = self.kwargs.get("contract_pk")
        connected_user_department = User.objects.filter(id=self.request.user.id).values(
            "department"
        )[0]["department"]
        # check user.department in ['S','M']
        # this is already checked thru permissions but we keep it in case we let thru to message

        if connected_user_department not in cts.SUPPORT_ENABLED_DEPARTMENT:
            error_message = f"""You, user {self.request.user}
             need to be member of Support, pls work on this with the support team."""
            raise ValidationError(error_message)

        # owasp : do not temper with contract in the data
        if contract_pk != target_contract:
            error_message = f"""you are not allowed to change the contract {target_contract},
             pls go back and select: {contract_pk}"""
            raise ValidationError(error_message)
        # check event_status is allowed
        if target_event_status not in cts.EVENT_PROGRESS_STATUS:
            error_message = f"""When updating an event, the satus can only be {cts.EVENT_OPEN},{cts.EVENT_WIP} or {cts.EVENT_CLOSED},
             pls correct."""
            raise ValidationError(error_message)
        # check support_contact mandatory
        if target_support_contact_id:
            error_message = f"""You {self.request.user} cannot change the support contact, pls remove the field."""
            raise ValidationError(error_message)

        super().perform_create(serializer, *args, **kwargs)
        logger.info(
            f"[{datetime.now()}]: Event.update {self.request.data} by {self.request.user}"
        )
