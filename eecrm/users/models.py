from django.db import models
from django.contrib.auth.models import AbstractUser

import base.constants as cts


class User(AbstractUser):
    # add a department attribute used for employees

    department = models.CharField(
        max_length=1,
        choices=cts.EMPLOYEEE_DEPARTMENT,
        default=cts.USER_EXTERNAL,
    )

    # account register history
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
