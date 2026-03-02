from django.db import models
from accounts.models import User
class Product(models.Model):
    store = models.ForeignKey('stores.Store', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
