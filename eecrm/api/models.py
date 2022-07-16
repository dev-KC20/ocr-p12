import base.constants as cts
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from django.db import models, IntegrityError

# from django.conf import settings

from users.models import User

# User = get_user_model()


def get_sentinel_user():
    # for RGPD & others reasons when a contributor is deleted one want to keep projects, issues or comments
    return get_user_model().objects.get_or_create(username="deletedUser")[0]


class Client(User):
    phone_number = RegexValidator(regex=r"^\+?1?\d{8,15}$", message=cts.PHONE_NOT_VALID)
    is_prospect = models.BooleanField(
        default=True,
        blank=False,
        null=False,
    )
    company_name = models.CharField(max_length=128, blank=False, null=False)
    company_phone = models.CharField(
        validators=[phone_number], max_length=16, blank=True
    )
    company_mobile = models.CharField(
        validators=[phone_number],
        max_length=16,
        blank=True,
    )
    sale_contact = models.ForeignKey(
        User,
        related_name="client_salesman",
        on_delete=models.PROTECT,
    )

    def __str__(self):
        return f"{self.company_name} "

    def save(self, *args, **kwargs):
        # surcharge to properly encrypt password
        user = super(Client, self)
        if user.password is not None and user.password != "":
            user.set_password(self.password)
        if user.username is not None:
            try:
                # in case instance is not unique
                user.save(*args, **kwargs)
            except IntegrityError:
                raise IntegrityError(
                    f"The Client username should be unique, pls change {user.username}."
                )


class Contract(models.Model):
    # true stands for when contract is signed else a draft
    status = models.BooleanField(
        default=False, blank=False, null=False, verbose_name="signed"
    )
    contract_name = models.CharField(max_length=128, blank=False, null=False)
    contract_amount = models.FloatField()
    payment_due = models.DateTimeField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    sale_contact = models.ForeignKey(
        User,
        related_name="contract_salesman",
        on_delete=models.PROTECT,
    )
    client = models.ForeignKey(
        Client,
        related_name="contract_client",
        on_delete=models.PROTECT,
    )

    def __str__(self):
        return self.contract_name


class Event(models.Model):

    event_status = models.CharField(
        max_length=1,
        choices=cts.EVENT_PROGRESS_STATUS,
        default=cts.EVENT_OPEN,
        blank=False,
        null=False,
    )
    attendees = models.IntegerField(
        default=50,
        null=False,
    )
    date_event = models.DateTimeField(
        blank=False,
        null=False,
    )
    notes = models.CharField(max_length=1024, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    support_contact = models.ForeignKey(
        User(),
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

    def get_event_attendees(self):
        return self.attendees
