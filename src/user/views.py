from rest_framework import generics
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from .serializers import UserSerializer, AuthTokenSerializer


class CreateUserApi(generics.CreateAPIView):
    """create new user"""
    serializer_class = UserSerializer


new_user = CreateUserApi.as_view()


class CreateTokenApi(ObtainAuthToken):
    """create new token for user"""
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


token = CreateTokenApi.as_view()
