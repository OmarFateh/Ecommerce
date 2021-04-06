from django.contrib import admin

from .models import Order, OrderItem

# models admin site registeration
admin.site.register(Order)
admin.site.register(OrderItem)