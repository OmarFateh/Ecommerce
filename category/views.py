from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse
from django.db.models import Max, Min
from django.template.loader import render_to_string

from .models import Category
from product.models import Product, Variation
from .utils import filter_products, paginate


def category_list(request, category_slug):
    """
    Take category slug, and get all products of this category.
    """
    # get category by its slug
    category = get_object_or_404(Category, slug=category_slug)
    # get category's ancestors including itself
    category_ancestors = category.get_ancestors(include_self=True)
    # get all products of descendants categories of this category
    products = Product.objects.get_descendants_products(category)
    # get all products ids of descendants categories of this category
    products_ids = Product.objects.get_descendants_products(category, ids=True)   
    # get all unduplicated colors of this category's products
    category_products_colors = Variation.objects.get_category_products_colors(category)
    # get all unduplicated sizes of this category's products
    category_products_sizes = Variation.objects.get_category_products_sizes(category)
    # get max & min brtween reguler and sale prices of of this category's products
    max_min_price = products.aggregate(Max('regular_price'), Min('regular_price'))
    max_min_sale_price = products.aggregate(Max('sale_price'), Min('sale_price'))
    max_price = max(max_min_price['regular_price__max'], max_min_sale_price['sale_price__max'])
    min_price = min(max_min_price['regular_price__min'], max_min_sale_price['sale_price__min'])
    # filter products by color & size & price
    size_ids = request.GET.getlist('size')
    color_ids = request.GET.getlist('color')
    price_range = request.GET.get('price')
    if size_ids or color_ids or price_range:
        products = filter_products(category_products_ids=products_ids, size_ids=size_ids, color_ids=color_ids, price_range=price_range) 
    # paginate products
    page_number = request.GET.get('page')
    if page_number:
        page_obj_products = paginate(products, page_number)
    else:
        page_obj_products = paginate(products)    
    if request.is_ajax():
        size_ids = request.GET.getlist('size[]')
        color_ids = request.GET.getlist('color[]')
        price_range = request.GET.get('price')
        page_number = request.GET.get('page')
        products = filter_products(category_products_ids=products_ids, size_ids=size_ids, color_ids=color_ids, price_range=price_range)
        page_obj_products = paginate(products, page_number)
        context = {'products':page_obj_products}
        data = dict()
        data['html_product_list'] = render_to_string('category/includes/partial_product_list.html', context)
        data['html_product_pagination'] = render_to_string('category/includes/partial_product_pagination.html', context)
        return JsonResponse(data)
    context = {
        'category':category, 
        'category_ancestors':category_ancestors, 
        'products':page_obj_products, 
        'category_products_colors':category_products_colors,
        'category_products_sizes':category_products_sizes,
        'max_price':max_price,
        'min_price':min_price,
        'size_ids':size_ids,
        'color_ids':color_ids,
    }
    return render(request, 'category/category_list.html', context)