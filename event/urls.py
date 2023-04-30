from django.urls import path
from event.views import index, by_event, new_event, delete_event, sign_event, update_event

urlpatterns = [
    path('', index, name='index'),
    path('index/', index, name='index'),
    path('event/<int:event_id>/', by_event, name='by_event'),
    path('newevent', new_event, name='newevent'),
    path('deleteevent/<int:event_id>/', delete_event, name='deleteevent'),
    path('signevent/<int:event_id>/', sign_event, name='signevent'),
    path('updateevent/<int:event_id>/', update_event, name='updateevent'),
]



