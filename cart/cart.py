from decimal import Decimal

from django.conf import settings

from product.models import Variation
from checkout.models import DeliveryOption
 

cart_session_id = settings.CART_SESSION_ID

class Cart():
    """
    A base Cart class, providing some default behaviors that can be inherited or overrided, as necessary.
    """
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(cart_session_id)
        if cart_session_id not in self.session:
            cart = self.session[cart_session_id] = {}
        self.cart = cart

    def __len__(self):
        """
        Get the cart data, and count the quantity of all items in the cart.
        """
        return sum(item['qty'] for item in self.cart.values())

    def __iter__(self):
        """
        Collect the product variation's id in the session data to query the database and return products' variations.
        """
        product_variation_ids = self.cart.keys()
        product_variations = Variation.objects.filter(id__in=product_variation_ids)
        cart = self.cart.copy()
        for variation in product_variations:
            cart[str(variation.id)]['variation_id'] = variation.id
            cart[str(variation.id)]['variation_product_url'] = variation.product.get_absolute_url
            cart[str(variation.id)]['variation_product_name'] = variation.product.name
            cart[str(variation.id)]['variation_color'] = variation.color.name
            cart[str(variation.id)]['variation_size'] = variation.size.name
            cart[str(variation.id)]['variation_image'] = variation.first_image.image.url
            cart[str(variation.id)]['variation_actual_price'] = float(variation.actual_price)
        for item in cart.values():
            item['price'] = float(item['price'])
            item['total_price'] = item['price'] * item['qty']
            yield item    

    def add(self, variation_id, qty, variation_actual_price=None):
        """
        Add and update the users cart session data.
        """
        product_variation_id = str(variation_id)
        if product_variation_id not in self.cart:
            # add new item to session data 
            self.cart[product_variation_id] = {'price': str(variation_actual_price), 'qty': qty}
        else:
            # update item in session data 
            self.cart[product_variation_id]['qty'] = qty 
        self.save()

    def delete(self, variation_id):
        """
        Delete item from session data.
        """
        product_variation_id = str(variation_id)
        if product_variation_id in self.cart:
            del self.cart[product_variation_id]
        self.save()

    def get_item_total_price(self, variation_id):
        """
        Get total price of all item in the cart.
        """
        product_variation_id = str(variation_id)
        item_price = float(self.cart[product_variation_id]['price'])
        return item_price * self.cart[product_variation_id]['qty']

    def get_total_price(self):
        """
        Get total price of all item in the cart.
        """
        return sum(float(item['price']) * item['qty'] for item in self.cart.values())

    def get_total_price_plus_first_delivery(self):
        """
        Get total price of all item in the cart after adding delivery price of first delivery option.
        """
        delivery_price = DeliveryOption.objects.first().price
        return self.cart_update_delivery(delivery_price)

    def cart_update_delivery(self, delivery_price=0):
        """
        Get total price of all item in the cart after adding delivery price.
        """
        return self.get_total_price() + float(delivery_price)

    def clear(self):
        """
        Clear all cart items from session data. 
        """
        del self.session[cart_session_id]
        del self.session['purchase']
        self.save()

    def save(self):
        """
        Save session data after updating it.
        """
        self.session.modified = True