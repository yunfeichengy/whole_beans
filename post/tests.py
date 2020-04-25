from django.utils import timezone
from django.test import TestCase
from django.test import Client

from .models import *

# Create your tests here.

class PostModelTests(TestCase):

    def test_product_is_made_or_updated_recently(self):
        product = Product(
            owner = None,
            name = 'p',
            description = 'a'*100,
            price =2.0,
            inventoryCount = 2,
            image=None,
            time=timezone.now()
        )

        t = product.is_updated_recently()
        self.assertIs(t, True)


    def test_sqLits_doesnt_enforce_max_length_limit(self):
        product = Product(
            owner = None,
            name = 'p',
            description = 'a'*3000,
            # note the max_length is set to 1000 for description
            # but sqLite does not enforce it
            # sqlite documentation:
            # https://www.sqlite.org/datatype3.html
            price =2.0,
            inventoryCount = 2,
            image=None,
            time=timezone.now()
        )

        length = len(product.get_description())
        test = length == 3000
        self.assertIs(test, True)

    def test_get_cart_items(self):
        product = Product(
            owner=User(),
            name='p',
            description='a' * 100,
            price=2.0,
            inventoryCount=2,
            image=None,
            time=timezone.now()
        )

        # create 3 orederItems
        item1 = OrderItem.objects.create(quantity=2)
        item2 = OrderItem.objects.create(quantity=2)
        item3 = OrderItem.objects.create(quantity=2)

        order = Order.objects.create(
            owner = None,
        )

        # add 3 items to Order
        order.items.add(item1)
        order.items.add(item2)
        order.items.add(item3)

        # check get_cart_items is working correctly
        length = len(order.get_cart_items())
        test = length == 3
        self.assertIs(test, True)
