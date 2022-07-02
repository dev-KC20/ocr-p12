from django.contrib.auth import get_user_model
from rest_framework.viewsets import ModelViewSet

from .models import Client, Contract, Event
from .permissions import EmployeeRole
from .serializers import ClientSerializer, ContractSerializer, EventSerializer

User = get_user_model()


class ClientViewSet(ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [EmployeeRole]


class ContractViewSet(ModelViewSet):
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer
    permission_classes = [EmployeeRole]


class EventViewSet(ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [EmployeeRole]
