from django.db.models import Q
from django.core.paginator import Paginator

from product.models import Product, Variation


def filter_products(category_products_ids, size_ids=None, color_ids=None, price_range=None):
    """
    """
    try:
        if price_range: 
            price_range_list = list(map(lambda x: int(x), price_range.replace('$', '').split('-')))  #price_range.replace('$', '').split('-')
            min_price_range = min(price_range_list)   #int(price_range_list[0])
            max_price_range = max(price_range_list)   #int(price_range_list[1])
        if size_ids and color_ids and price_range:
            # filter products variation by color & size & price
            products_variation = Variation.objects.filter(product__id__in=category_products_ids, size__id__in=size_ids, color__id__in=color_ids).filter(
                Q(product__regular_price__range=(min_price_range,max_price_range))|
                Q(product__sale_price__range=(min_price_range,max_price_range))
            ).distinct()
        elif color_ids and price_range:
            # filter products variation by color & price
            products_variation = Variation.objects.filter(product__id__in=category_products_ids, color__id__in=color_ids).filter(
                Q(product__regular_price__range=(min_price_range,max_price_range))|
                Q(product__sale_price__range=(min_price_range,max_price_range))
            ).distinct()
        elif size_ids and price_range:
            # filter products variation by price & size
            products_variation = Variation.objects.filter(product__id__in=category_products_ids, size__id__in=size_ids).filter(
                Q(product__regular_price__range=(min_price_range,max_price_range))|
                Q(product__sale_price__range=(min_price_range,max_price_range))
            ).distinct()
        elif size_ids and color_ids:
            # filter products variation by color & size
            products_variation = Variation.objects.filter(color__id__in=color_ids, size__id__in=size_ids, product__id__in=category_products_ids)
        elif color_ids: 
            # filter products variation by color
            products_variation = Variation.objects.filter(color__id__in=color_ids, product__id__in=category_products_ids)
        elif size_ids:    
            # filter products variation by size
            products_variation = Variation.objects.filter(size__id__in=size_ids, product__id__in=category_products_ids)
        elif price_range:
            # filter products variation by price
            products_variation = Variation.objects.filter(product__id__in=category_products_ids).filter(
                Q(product__regular_price__range=(min_price_range,max_price_range))|
                Q(product__sale_price__range=(min_price_range,max_price_range))
            ).distinct()
        else:
            products_variation = Variation.objects.filter(product__id__in=category_products_ids)
    except:
        products_variation = Variation.objects.filter(product__id__in=category_products_ids)        
    products_ids = Variation.objects.get_products_ids(products_variation)
    return Product.objects.filter(id__in=products_ids)

def paginate(qs, page_number=1):
    """
    Take a queryset, and page number with a default value of 1, and paginate the queryset.
    """
    paginator_qs = Paginator(qs, 1) # display 10 objects per page.
    return paginator_qs.get_page(page_number)
    # try:
    #     paginated_objs = paginator_qs.get_page(page_number)
    # except PageNotAnInteger:
    #     paginated_objs = paginator.page(1)
    # except EmptyPage:
    #     paginated_objs = paginator.page(paginator.num_pages)
    # return paginated_objs