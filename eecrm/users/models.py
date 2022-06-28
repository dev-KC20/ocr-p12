from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    pass


class Employee(User):
    # a project owner is a project author

    SALES = "S"
    SUPPORT = "A"
    MANAGEMENT = "M"
    EMPLOYEEE_DEPARTMENT = [
        (SALES, "Commercial"),
        (SUPPORT, "Assistance"),
        (MANAGEMENT, "Gestion"),
    ]

    department = models.CharField(
        max_length=1,
        choices=EMPLOYEEE_DEPARTMENT,
        default=SALES,
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        """ The management employee need more rights than others as per specifications
            'Créer, mettre à jour et supprimer des utilisateurs dans le système CRM.
             Afficher et modifier toutes les données dans le système CRM.'
        """
        employee = super(Employee, self)
        if self.department == self.MANAGEMENT:
            self.is_staff = True
            self.is_superuser = True
        else:
            self.is_staff = False
            self.is_superuser = False
        # password actually required and hashed
        if len(self.password) != 0:
            employee.set_password(self.password)
        employee.save()
        return employee
