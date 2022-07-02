from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    # add a department attribute used for employees
    EXTERNAL = "E"
    SALES = "S"
    SUPPORT = "A"
    MANAGEMENT = "M"
    EMPLOYEEE_DEPARTMENT = [
        (EXTERNAL, "Partenaire"),
        (SALES, "Commercial"),
        (SUPPORT, "Assistance"),
        (MANAGEMENT, "Gestion"),
    ]

    department = models.CharField(
        max_length=1,
        choices=EMPLOYEEE_DEPARTMENT,
        default=SALES,
    )
    

# account register history
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)