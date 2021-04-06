import stripe
import json

from django.conf import settings
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import get_user_model
from django.core.mail import EmailMessage, BadHeaderError
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from cart.cart import Cart
from order.models import Order, OrderItem
from order.forms import AddOrderForm
from product.models import Variation
from .models import DeliveryOption
from .decorators import empty_cart

User = get_user_model()
stripe.api_key = settings.STRIPE_SECRET_KEY

@login_required
@empty_cart
def checkout(request):
    """
    Display checkout form.
    """
    cart = Cart(request)
    delivery_options = DeliveryOption.objects.get_active_options()
    order_form = AddOrderForm(request.POST or None)
    context = {
        'delivery_options':delivery_options,
        'form':order_form, 
        "stripe_pk": settings.STRIPE_PUBLIC_KEY, 
    }
    return render(request, 'payment/checkout.html', context)

@login_required
def create_order(request):
    """
    Create order with stripe as a payment geteway.
    """
    cart = Cart(request)
    # total_price = cart.get_total_price()
    delivery_option_id = int(request.POST.get("delivery_option"))
    delivery_type = get_object_or_404(DeliveryOption, id=delivery_option_id)
    updated_total_price = cart.cart_update_delivery(delivery_type.price)
    total_price_int = int(updated_total_price * 100)
    # create stripe intent
    intent = stripe.PaymentIntent.create(
        amount=total_price_int,
        currency='usd',
        metadata={
            "user_id": request.user.id
        }
    )
    # add order 
    data = dict()
    order_form = AddOrderForm(request.POST or None)
    if order_form.is_valid():
        data['form_is_valid'] = True
        # check if order exists with the order key
        order_key = intent.client_secret
        if not Order.objects.filter(order_key__iexact=order_key).exists():
            # create new order 
            order = order_form.save(commit=False)
            order.user = request.user
            order.delivery_option = delivery_type
            order.total_paid = cart.get_total_price()
            order.order_key = order_key
            order.save() 
            # create new item order for each item in the cart 
            for item in cart:
                OrderItem.objects.create(order_id=order.pk, variation_id=item['variation_id'], price=item['price'], quantity=item['qty'])
                # update variation qty in stock
                item_variation = Variation.objects.get(id=item['variation_id'])
                item_variation.quantity -= item['qty']
                # update product qty in stock
                item_variation.product.quantity -= item['qty']
            data["client_secret"] = order_key    
    return JsonResponse(data)

@login_required
def update_delivery_cart(request):
    """
    Get selected delivery option, and update the total price in the cart.
    """
    cart = Cart(request)
    delivery_option_id = int(request.POST.get("delivery_option"))
    delivery_type = get_object_or_404(DeliveryOption, id=delivery_option_id)
    updated_total_price = cart.cart_update_delivery(delivery_type.price)
    # add purchase to sessions.
    session = request.session
    if "purchase" not in session:
        # create new one. 
        session["purchase"] = {"delivery_id": delivery_type.id}
    else:
        # update the old one.
        session["purchase"]["delivery_id"] = delivery_type.id
        session.modified = True
    data = {"total_price": updated_total_price, "delivery_price": delivery_type.price}    
    return JsonResponse(data)

@csrf_exempt
def stripe_webhook(request):
    """
    Stripe webhook view.
    """
    payload = request.body
    event = None

    try:
        event = stripe.Event.construct_from(
            json.loads(payload), stripe.api_key
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the event
    if event.type == 'payment_intent.succeeded':
        # update order billing status
        order = Order.objects.payment_confirmation(event.data.object.client_secret)
        # send email to customer.
        # EmailMessage( subject, message, email_from, recipient_list )
        user = get_object_or_404(User, pk=event.data.object.metadata.user_id)
        try:
            email = EmailMessage(
                f'Purchasing Products Confirmation', # subject  
                f"""Hello {user.first_name} {user.last_name}, 
                \nthank you for your purchase with total of ${order.total_paid},
                \nand here is your order details: 
                \nproduct1\n \n \n \nBest Regards \nAvone Team""", # message
                'fatehomar0@gmail.com', # from email
                [user.email,] # to email list
            )
            email.send(fail_silently=False)
        except BadHeaderError:
            return HttpResponse('Invalid header found.')  
    return HttpResponse(status=200)

@login_required
def order_placed(request):
    """
    Clear cart after the oder has been placed.
    """
    cart = Cart(request)
    cart.clear()
    return render(request, 'payment/order_placed.html', {})