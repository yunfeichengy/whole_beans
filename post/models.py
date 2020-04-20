from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)  # each post is a foreign key to a user
    title = models.CharField(max_length=100)
    content = models.CharField(max_length=10000)
    created = models.DateTimeField(auto_now_add=True)   # means I don't manually specify a date each time it's created


class Product(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    price = models.FloatField()
    inventoryCount = models.IntegerField()
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class OrderItem(models.Model):
    product = models.OneToOneField(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField()

    def __str__(self):
        return self.product.name


class Order(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)

    def get_cart_items(self):
        return self.items.all()

    def get_cart_total(self):
        sumVar = 0
        for item in self.items.all():
            sumVar += item.quantity * item.product.price
        return sumVar

    def __str__(self):
        return self.owner.username
