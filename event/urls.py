from django.urls import path
from event.views import index, by_event, new_event, delete_event, sign_event, update_event, update_userevent, delete_userevent

urlpatterns = [
    path('', index, name='index'),
    path('index/', index, name='index'),
    path('event/<int:event_id>/', by_event, name='by_event'),
    path('newevent', new_event, name='newevent'),
    path('deleteevent/<int:event_id>/', delete_event, name='deleteevent'),
    path('signevent/<int:event_id>/', sign_event, name='signevent'),
    path('updateevent/<int:event_id>/', update_event, name='updateevent'),
    path('updateuserevent/<int:ue_id>/', update_userevent, name='updateuserevent'),
    path('deleteuserevent/<int:ue_id>/', delete_userevent, name='deleteuserevent'),
]



