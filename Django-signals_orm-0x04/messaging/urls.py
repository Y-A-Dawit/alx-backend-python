from django.urls import path
from .views import user_messages_with_replies

urlpatterns = [
    path('messages/threaded/', user_messages_with_replies, name='threaded-messages'),
]
