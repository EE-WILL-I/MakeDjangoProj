from django.urls import path
from .views import signup
from .views import update_user

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('update/', update_user, name='update_user')
]