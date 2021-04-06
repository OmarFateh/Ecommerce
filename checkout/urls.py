from django.urls import path

from checkout.views import checkout, create_order, update_delivery_cart, stripe_webhook, order_placed

# namespace = checkout

urlpatterns = [
    path('checkout/', checkout, name='checkout'),
    path("ajax/order/create/", create_order, name="ajax-create-order"),
    path("ajax/delivery/cart/update/", update_delivery_cart, name="ajax-update-delivery-cart"),
    path('webhooks/stripe/', stripe_webhook, name='stripe-webhook'),
    path('checkout/orderplaced/', order_placed, name='order-placed'),
]