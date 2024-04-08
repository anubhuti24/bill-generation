from django.db import models


class Item(models.Model):
    id = models.AutoField(primary_key=True)
    item_name = models.CharField(max_length=30)
    item_price = models.IntegerField()
    description = models.CharField(max_length=50)
