from django.urls import path
from .views import signup

urlpatterns = [
    path('test1/', signup, name='test1'),
]