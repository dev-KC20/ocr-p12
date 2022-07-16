# import the logging library
import logging
from datetime import datetime
from django.contrib.auth.forms import UserCreationForm
from .models import User

# Get an instance of a logger
logger = logging.getLogger(__name__)


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
        user.is_active = True
        # password required and hashed
        try:

            user.set_password(self.cleaned_data["password1"])
        except AttributeError:  # Be explicit with catching exceptions.
            logger.info(
                f"[{datetime.now()}]: User.Create password mismatch, no action needed."
            )

        user.save()
        logger.info(f"[{datetime.now()}]: User.Create {user.username,} ")
        return user


# class CustomUserChangeForm(UserChangeForm):

#     def save(self, commit=True):
#         """ Here the concern is only trace who changes a user
#             owasp
#         """
#         user = super().save(commit=True)
#         # logger.info(f"[{datetime.now()}]: User.Update {user.username,} by {request.user}")
#         return user
