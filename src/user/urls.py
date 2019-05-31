from django.urls import path

from .views import new_user, token

app_name = 'user'
urlpatterns = [
    path('create/', new_user, name='new_user'),
    path('token/', token, name='token'),
]
