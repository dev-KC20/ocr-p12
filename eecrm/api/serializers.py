from rest_framework.serializers import ModelSerializer

from .models import Client, Contract, Event


class ClientSerializer(ModelSerializer):
    class Meta:
        model = Client
        fields = [
            "id",
            "is_prospect",
            "company_name",
            "company_phone",
            "company_mobile",
            "sale_contact",
            "first_name",
            "last_name",
            "email",
            "is_active",
            "date_created",
            "date_updated",
            "username",
        ]


class ContractSerializer(ModelSerializer):
    class Meta:
        model = Contract
        fields = [
            "id",
            "status",
            "contract_name",
            "contract_amount",
            "payment_due",
            "date_created",
            "date_updated",
            "sale_contact",
            "client",
        ]


class EventSerializer(ModelSerializer):
    class Meta:
        model = Event
        fields = "__all__"
