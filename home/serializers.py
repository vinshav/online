from rest_framework import serializers
from .models import *
from django.contrib.auth.hashers import make_password

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'name', 'email', 'password')
        extra_kwargs = {
                'password': {'write_only': True}  # For write only perpose, it wont be displayed to user
            }
        def create(self, user_data):
            password = user_data.pop('password', None)

            if password is not None:
                instance.make_password(password)
            instance = self.Meta.model(**user_data)
            instance.save()
            
            return instance