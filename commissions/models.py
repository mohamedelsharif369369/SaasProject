from django.db import models
from orders.models import OrderItem
class Commission(models.Model):
    order_item = models.ForeignKey(OrderItem,on_delete=models.CASCADE)
    percentage = models.DecimalField(max_digits=5,decimal_places=2)
    amount = models.DecimalField(max_digits=10,decimal_places=2)
