"""
Serialisers file.
"""
from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer
from rest_framework import serializers
from rest_framework.fields import CharField, DateTimeField, DecimalField, IntegerField

from Traders.models import History, Stock

User = get_user_model()


class CustomUserCreateSerializer(UserCreateSerializer):
    """
    .
    """

    class Meta(UserCreateSerializer.Meta):
        """
        .
        """
        model = User
        fields = ('id', 'username', 'email', 'password')


class StockSerializer(serializers.ModelSerializer):
    company = CharField(max_length=100)
    quantity = IntegerField(min_value=1)
    class Meta:
        model = Stock
        fields = ['company', 'quantity']


class HistorySerializer(serializers.Serializer):
    company = CharField(max_length=100)
    quantity = IntegerField(min_value=1)
    price = DecimalField(max_digits=20, decimal_places=2)
    type = CharField(max_length=1)
    time = DateTimeField(format='%d/%m/%y %H:%M:%S')
    class Meta:
        model = History
        fields = ['company', 'quantity', 'price', 'type', 'time']
