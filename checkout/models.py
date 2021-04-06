from django.db import models

from product.models import BaseTimestamp


class DeliveryOptionManager(models.Manager):
    """
    Delivery Option model manager.
    """
    def get_active_options(self):
        """
        Get all active delivery options.
        """
        return self.get_queryset().filter(active=True)


class DeliveryOption(BaseTimestamp):
    """
    Delivery options model.
    """
    DELIVERY_CHOICES = [
        ("IS", "In Store"),
        ("HD", "Home Delivery"),
        ("DD", "Digital Delivery"),
    ]

    name = models.CharField(max_length=64)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    method = models.CharField(max_length=32, choices=DELIVERY_CHOICES)
    timeframe = models.CharField(max_length=64)
    list_order = models.IntegerField(default=0)
    active = models.BooleanField(default=True)

    objects = DeliveryOptionManager()

    class Meta:
        ordering = ['list_order']

    def __str__(self):
        # Return name.
        return self.name


class PaymentMethod(BaseTimestamp):
    """
    Payment methods model.
    """
    name = models.CharField(max_length=64)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        # Return name.
        return self.name