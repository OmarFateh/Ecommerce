from django.urls import path

from .views import cart_summary, cart_add, cart_update_delete

# namespace = cart

urlpatterns = [
    path('cart/', cart_summary, name='cart-summary'),
    path('ajax/cart/add/', cart_add, name='cart-add'),
    path('ajax/cart/update/delete/', cart_update_delete, name='cart-update-delete'),
]