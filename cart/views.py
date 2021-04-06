from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.template.loader import render_to_string

from product.models import Variation
from .cart import Cart


def cart_summary(request):
    """
    Display user's cart summary.
    """
    return render(request, 'cart/cart_summary.html', {})

def cart_add(request):
    """
    Add item to cart.
    """
    cart = Cart(request)
    product_id = int(request.POST.get("product_id"))
    size_id = int(request.POST.get("size_id"))
    color_id = int(request.POST.get("color_id"))
    product_variation = Variation.objects.filter(product__id=product_id, size__id=size_id, color__id=color_id).first()
    product_variation_qty = int(request.POST.get("product_qty"))
    cart.add(variation_id=product_variation.id, qty=product_variation_qty, variation_actual_price=product_variation.actual_price)
    data = dict() 
    data['html_mini_cart_data'] = render_to_string('cart/includes/partial_mini_cart.html', {'cart':cart})
    data['qty'] = cart.__len__()
    return JsonResponse(data)
   
def cart_update_delete(request):
    """
    Update and delete item from cart.
    """
    cart = Cart(request)
    variation_id = int(request.POST.get("variation_id"))
    data = dict()
    # update item.
    if request.POST.get('action') == 'update':
        product_variation_qty = int(request.POST.get("product_qty"))
        cart.add(variation_id=variation_id, qty=product_variation_qty)
        data['item_total_price'] = cart.get_item_total_price(variation_id)
        data['cart_total_price'] = cart.get_total_price() 
    # delete item.
    elif request.POST.get('action') == 'delete':
        cart.delete(variation_id=variation_id)
        context = {'cart':cart}
        data['html_mini_cart_data'] = render_to_string('cart/includes/partial_mini_cart.html', context)
        data['html_cart_data'] = render_to_string('cart/includes/partial_cart_summary.html', context)
    data['cart_qty'] = cart.__len__()
    return JsonResponse(data)   