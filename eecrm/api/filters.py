from django.db import models
from rest_framework import generics
from django_filters import rest_framework as filters
from django_filters import CharFilter
from .models import Contract


class ContractFilter(filters.FilterSet):
    min_contract_amount = filters.NumberFilter(
        field_name="contract_amount", lookup_expr="gte"
    )
    max_contract_amount = filters.NumberFilter(
        field_name="contract_amount", lookup_expr="lte"
    )
    min_payment_due = filters.DateFilter(
        field_name="payment_due", lookup_expr="gte"
    )
    max_payment_due = filters.DateFilter(
        field_name="payment_due", lookup_expr="lte"
    )
    # payment_due = filters.IsoDateTimeFromToRangeFilter

    class Meta:
        model = Contract
        fields = [
            "contract_name",
            "contract_amount",
            "min_contract_amount",
            "max_contract_amount",
            "client__email",
            "client__company_name",
            "payment_due",
            "min_payment_due",
            "max_payment_due",
        ]

        filter_overrides = {
            models.CharField: {
                "filter_class": CharFilter,
                "extra": lambda f: {
                    "lookup_expr": "icontains",
                },
            },
        }
