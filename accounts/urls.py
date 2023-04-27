from django.urls import path
from .views import SignUpView, update_users

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup1'),
    path('signup/', update_users, name='signup2'),
]