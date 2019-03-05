from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Ticket


class TicketSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Ticket
        fields = ('url', 'id', 'title', 'text', 'owner')


class UserSerializer(serializers.ModelSerializer):
    tickets = serializers.HyperlinkedRelatedField(many=True, view_name='ticket-detail', read_only=True)

    class Meta:
        model = User
        fields = ('url', 'id', 'username', 'tickets')
