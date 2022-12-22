from django.http import HttpResponse
from . import tasks
from rest_framework import generics
from .models import Order
from .serializers import OrderSerizalizer


def home(request):
    tasks.get_parsed_data.delay()
    return HttpResponse('<h1>Загружаю данные</h1>')


class OrderApiView(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerizalizer
