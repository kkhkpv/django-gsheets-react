from django.db import models


class Order(models.Model):
    order_number = models.CharField(max_length=255)
    cost = models.IntegerField()
    delivery_date = models.DateField()
    rouble_cost = models.IntegerField()

    def __str__(self) -> str:
        return self.order_number
