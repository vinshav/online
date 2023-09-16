from rest_framework.views import APIView
from .models import *
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
# Create your views here.
from .serializers import *
# import jwt
import datetime
from django.core.files.storage import FileSystemStorage
from django.core.files.storage import default_storage
from PIL import Image, ImageOps
import os
from rest_framework import permissions

JWT_SECRET="DFSDFDSFJ23LJ32"

class RegisterView(APIView):
    def post(self, request):
        serializers = UserSerializer(data = request.data)
        serializers.is_valid(raise_exception = True)
        serializers.save()
        return Response({
            'status' : 'ok',
            'message' : 'Registered success'
        })
    
        
class LoginView(APIView):

    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        user = User.objects.filter(email=email).first()
        if user is None:
            raise AuthenticationFailed('user not found')

        checkpass = User.objects.filter(password=password).first()
        if checkpass is None:
            raise AuthenticationFailed('wrong password')

        payload = {
            'id': user.id,
            # expired in  1 minute
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow(),
            'email' : user.email,
            'name' : user.name,
        }
        token = jwt.encode(payload, JWT_SECRET, algorithm='HS256')
        res = Response()
        # res.set_cookie(key='jwt', value=token, httponly=True)
        res.data = {
            'jwt':  token,
        }

        return res