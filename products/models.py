from django.db import models


class Product(models.Model):
    product_name = models.CharField(max_length=255, unique=True)
    product_quantity = models.PositiveIntegerField()

    def save(self, *args, **kwargs):
        self.product_name = self.product_name.lower()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.product_name


class Bundle(models.Model):
    name = models.CharField(max_length=255)
    products = models.ManyToManyField(Product)
    stock = models.PositiveIntegerField()

    def __str__(self):
        return self.name


class SalesChannel(models.Model):
    sales_channel_name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.sales_channel_name


