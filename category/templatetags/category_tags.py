from django import template

from product.models import Variation, Product, ProductImage

register = template.Library()

@register.simple_tag
def remove_duplicated_colors(products_qs):
    """
    Take a queryset of products, and get unduplicated colors of these products variations.
    """
    return products_qs.order_by('color').values('color__id', 'color__name', 'color__code').distinct()

@register.simple_tag
def is_in(var, lst):
    """
    Take variable and list of objects, and check if the variable is in the list.
    """
    return str(var) in lst

@register.simple_tag
def get_product_thumbnails(product_id):
    """
    Take product's id, and get first two thumbnails images of this product.
    """
    return ProductImage.objects.get_thumbnails(product_id)

@register.simple_tag
def get_product_thumbnail(product_id):
    """
    Take product's id, and get first thumbnail images of this product.
    """
    return ProductImage.objects.get_favourite_list_thumbnail(product_id)

@register.simple_tag
def redirected_url(spliter, urlencode=None):
    """
    """
    querystring = urlencode.split(spliter) 
    return querystring[1:]   