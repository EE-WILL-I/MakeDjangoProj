from django.urls import path
from event.views import index, by_event

urlpatterns = [
    path('', index, name='index'),
    path('<int:event_id>/', by_event, name='by_event'),
]



