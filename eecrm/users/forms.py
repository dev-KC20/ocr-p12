from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
# import the logging library
import logging

from .models import User
import base.constants as cts




class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = "__all__"

    def save(self, commit=True):
        """The management employee need more rights than others as per specifications
        'Créer, mettre à jour et supprimer des utilisateurs dans le système CRM.
         Afficher et modifier toutes les données dans le système CRM.'
        """
        # Get an instance of a logger
        logger = logging.getLogger(__name__)

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
        logger.warning('save user name, dpt, active,staff:', user.username, user.department, user.is_active, user.is_staff,)
        # print('save user name, dpt, active,staff:', user.username, user.department, user.is_active, user.is_staff,)
        # password required and hashed
        if user.password is not None:
            if self.password1 is not None:
                user.set_password(self.password1)
            if self.password is not None:
                user.set_password(self.password)

        # managers = Group.objects.get_or_create(name=user.department)
        # print('admin managers group', managers[0])
        # manager = managers[0]
        user.save()
        # manager.save()
        # manager.user_set.add(user)
        return user
