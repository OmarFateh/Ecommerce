from django.db import models
from django.conf import settings

from product.models import BaseTimestamp
from checkout.models import DeliveryOption, PaymentMethod


class OrderManager(models.Manager):
    """
    Order model manager
    """
    def paid_orders(self):
        """
        Get all paid orders.
        """
        return self.get_queryset().filter(billing_status=True)

    def payment_confirmation(self, order_key):
        """
        Take order key, and get its order and update the billing status to be ture.
        """
        order = self.get_queryset().filter(order_key__iexact=order_key)
        order.update(billing_status=True)
        return order.first()

    def user_orders(self, user_id):
        """
        Take user's id, and get his all paid orders.
        """
        return self.paid_orders().filter(user__id=user_id)

    def get_user_orders_products_ids(self, user_id):
        """
        Take user's id, and get list of his order's products ids.
        """
        products_list_ids = []
        for order in self.user_orders(user_id):
            for item in order.items.all():
                if item.variation.product.id not in products_list_ids:
                    products_list_ids.append(item.variation.product.id)  
        return products_list_ids


class Order(BaseTimestamp):
    """
    Order model.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='orders', null=True)
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.SET_NULL, related_name='orders', null=True)
    delivery_option = models.ForeignKey(DeliveryOption, on_delete=models.SET_NULL, related_name='orders', null=True)
    full_name = models.CharField(max_length=64)
    address1 = models.CharField(max_length=250)
    address2 = models.CharField(max_length=250)
    city = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)
    post_code = models.CharField(max_length=20)
    total_paid = models.DecimalField(max_digits=10, decimal_places=2)
    order_key = models.CharField(max_length=200, unique=True)
    billing_status = models.BooleanField(default=False)

    objects = OrderManager()

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        # Return user's name and date of order creation. 
        return  f"{self.full_name} | {self.created_at}"  


class OrderItem(BaseTimestamp):
    """
    Order item model.
    """
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    variation = models.ForeignKey("product.Variation", on_delete=models.CASCADE, related_name='order_items')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        # Return order item's id. 
        return  f"{self.id}"

    def get_total_price(self):
        # Return total price of all quantities.
        return self.price * self.quantity    