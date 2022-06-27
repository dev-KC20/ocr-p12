# from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import User
# User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = User
        fields = '__all__'
