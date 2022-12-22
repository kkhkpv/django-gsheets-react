from rest_framework import serializers
from .models import Order


class OrderSerizalizer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('order_number', 'cost', 'delivery_date', 'rouble_cost')
