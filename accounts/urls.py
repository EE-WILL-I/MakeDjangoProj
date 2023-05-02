from django.urls import path
from .views import signup
from .views import update_user, by_account, delete_account

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('update/', update_user, name='update_user'),
    path('account/<int:user_id>/', by_account, name='by_account'),
    path('deleteaccount/<int:user_id>/', delete_account, name='delete_account'),
]
