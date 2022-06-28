import base.constants as cts
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from django.db import models
from users.models import Employee

User = get_user_model()


def get_sentinel_user():
    # for RGPD & others reasons when a contributor is deleted one want to keep projects, issues or comments
    return get_user_model().objects.get_or_create(username="deletedUser")[0]


class Client(User):
    is_prospect = models.BooleanField(
        default=True,
        blank=False,
        null=False,
    )
    company_name = models.CharField(max_length=128, blank=False, null=False)
    company_phone = RegexValidator(regex=r"^\+?1?\d{8,15}$", message=cts.PHONE_NOT_VALID)
    company_mobile = RegexValidator(regex=r"^\+?1?\d{8,15}$", message=cts.PHONE_NOT_VALID)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    sale_contact = models.ForeignKey(
        Employee,
        related_name="client_salesman",
        on_delete=models.PROTECT,
    )

    def __str__(self):
        return self.company_name


class Contract(models.Model):
    # true stands for when contract is signed else a draft
    status = models.BooleanField(default=False, blank=False, null=False, verbose_name="signed")
    contract_name = models.CharField(max_length=128, blank=False, null=False)
    contract_amount = models.FloatField()
    payment_due = models.DateTimeField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    sale_contact = models.ForeignKey(
        Employee,
        related_name="contract_salesman",
        on_delete=models.PROTECT,
    )
    client = models.ForeignKey(
        Client,
        related_name="contract_client",
        on_delete=models.PROTECT,
    )

    def __str__(self):
        return f"{self.contract.contract_name} for {self.client.company_name} status on {self.status}."


class Event(models.Model):

    OPEN = "C"
    WIP = "E"
    CLOSED = "T"
    EVENT_PROGRESS_STATUS = [
        (OPEN, "Créé"),
        (WIP, "En cours"),
        (CLOSED, "Terminé"),
    ]
    event_status = models.CharField(
        max_length=1,
        choices=EVENT_PROGRESS_STATUS,
        default=OPEN,
    )
    attendees = models.IntegerField()
    date_event = models.DateTimeField()
    notes = models.CharField(max_length=1024, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    support_contact = models.ForeignKey(
        Employee,
        related_name="event_manager",
        on_delete=models.PROTECT,
    )
    contract = models.ForeignKey(
        Contract,
        related_name="event_contract",
        on_delete=models.PROTECT,
    )

    def __str__(self):
        return f"The {self.contract.contract_name} event on {self.date_event} with {self.attendees} attendees"
