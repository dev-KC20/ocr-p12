from django.db import models
from rest_framework import generics
from django_filters import rest_framework as filters
from django_filters import CharFilter
from .models import Contract


class ContractFilter(filters.FilterSet):
    min_contract_amount = filters.NumberFilter(field_name="contract_amount", lookup_expr="gte")
    max_contract_amount = filters.NumberFilter(field_name="contract_amount", lookup_expr="lte")

    class Meta:
        model = Contract
        fields = ["contract_name", "contract_amount", "min_contract_amount", "max_contract_amount"]

        filter_overrides = {
            models.CharField: {
                "filter_class": CharFilter,
                "extra": lambda f: {
                    "lookup_expr": "icontains",
                },
            },
        }
