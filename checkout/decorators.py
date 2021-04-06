from django.shortcuts import redirect
from django.urls import reverse

from cart.cart import Cart


def empty_cart(view_func):
    """
    Restrict the user from visiting checkout page if the cart is empty,
    Redirect to cart page. 
    """
    def wrapper_func(request, *args, **kwargs):
        cart = Cart(request)
        if cart.__len__():
            return view_func(request, *args, **kwargs)
        else: 
            return redirect(reverse("cart:cart-summary"))   
    return wrapper_func  