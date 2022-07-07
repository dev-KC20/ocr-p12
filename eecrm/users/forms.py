# import the logging library
import logging
from datetime import datetime
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import Group
from .models import User
import base.constants as cts

# Get an instance of a logger
logger = logging.getLogger(__name__)

# logger.info(f"[{datetime.now()}]:  Usercreationform")


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = "__all__"

    def save(self, commit=True):
        """The management employee need more rights than others as per specifications
        'Créer, mettre à jour et supprimer des utilisateurs dans le système CRM.
         Afficher et modifier toutes les données dans le système CRM.'
        """
        user = super().save(commit=False)
        if user.department == cts.USER_MANAGEMENT:
            user.is_superuser = True
        else:
            user.is_superuser = False
        if user.department == cts.USER_EXTERNAL:
            user.is_staff = False
        else:
            user.is_staff = True

        user.is_active = True
        # password required and hashed
        if user.password is not None:
            if self.password1 is not None:
                user.set_password(self.password1)
            if self.password is not None:
                user.set_password(self.password)

        user.save()
        logger.info(f"[{datetime.now()}]: User.Create {user.username,} by {self.request.user}")
        return user

class CustomUserChangeForm(UserChangeForm):

    def save(self, commit=True):
        """ Here the concern is only trace who changes a user
            owasp
        """
        user = super().save(commit=True)
        logger.info(f"[{datetime.now()}]: User.Update {user.username,} by {self.request.user}")
        return user
