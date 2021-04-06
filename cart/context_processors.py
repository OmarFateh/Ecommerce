from .cart import Cart

def cart(request):
    """
    Custom context processor for cart.
    """
    return {'cart':Cart(request)}  