import django_filters
from .models import Message

class MessageFilter(django_filters.FilterSet):
    sender = django_filters.CharFilter(field_name='sender__user_id', lookup_expr='exact')
    conversation = django_filters.CharFilter(field_name='conversation__conversation_id', lookup_expr='exact')
    date_from = django_filters.DateTimeFilter(field_name='timestamp', lookup_expr='gte')
    date_to = django_filters.DateTimeFilter(field_name='timestamp', lookup_expr='lte')

    class Meta:
        model = Message
        fields = ['sender', 'conversation', 'date_from', 'date_to']
