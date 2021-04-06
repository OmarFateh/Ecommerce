import json

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.db.models import Avg

from order.models import Order
from .forms import AddReviewForm
from .models import Product, Variation, ProductImage, ProductReview 
from .utils import Round, get_product_reviews_avg_rate


def product_detail(request, product_slug=None):
    """
    Take slug, get the product with this slug, and display the product detail.
    Create comment or reply to this product.
    """
    # get product by its slug.
    product = get_object_or_404(Product, slug=product_slug)    
    # get all product's categories including itself.
    categories = product.category.get_ancestors(include_self=True)
    # get all available sizes of this product.
    product_sizes = Variation.objects.get_product_sizes(product_id=product.id)
    product_colors = None
    first_color = None
    first_size  = None
    product_images = None
    first_image  = None
    if product_sizes:
        # get first product size.
        first_size = product_sizes[0]['name']
        # get all colors of first product size.
        product_colors = Variation.objects.get_size_color_list(product_id=product.id, size_id=product_sizes[0]['id'])
        # get first color of first product size.
        first_color = product_colors[0]['name']
        # get all images of first product size.
        product_images = ProductImage.objects.filter(variation__size__id=product_sizes[0]['id'], variation__product__id=product.id)
        # get first product image.
        first_image = product_images.first() 
    # get product's reviews
    product_reviews = ProductReview.objects.filter(product=product)
    product_reviews_count = product_reviews.count()
    # get product average rate
    try:
        product_avg_rate = int(product_reviews.aggregate(rounded_avg_price=Round(Avg('rate')))['rounded_avg_price'])*20
    except:
        product_avg_rate = 0
    # add new review form
    review_form = AddReviewForm()
    # check if user is logged in, has ordered this product and hasn't added a review yet.
    # get user's review for this product.
    if request.user.is_authenticated:
        user_product_review = ProductReview.objects.filter(user=request.user, product=product).first()
        is_review_exists = False
        if user_product_review:
            is_review_exists = True
        # get ids list of products which the user has ordered 
        user_orders_products_ids_list = Order.objects.get_user_orders_products_ids(request.user.id)
        is_review_allowed = False
        if product.id in user_orders_products_ids_list:
            is_review_allowed = True
    else:
        user_product_review = None
        is_review_exists = False
        is_review_allowed = False

    context = {
        "product":product, 
        "categories":categories,
        "product_colors":product_colors, 
        'first_color':first_color,
        "product_sizes":product_sizes, 
        'first_size':first_size,
        'product_images':product_images,
        'first_image':first_image,
        'form':review_form,
        'reviews':product_reviews,
        'reviews_count':product_reviews_count,
        'avg_rate_precentage':product_avg_rate,
        "user_product_review":user_product_review,
        "is_review_allowed":is_review_allowed,
        'is_review_exists':is_review_exists,
        }
    return render(request, 'product/product_detail.html', context)


def product_variation(request, product_id=None):
    """
    Take product's id, and get all its variations.
    """
    variation_list_data = Variation.objects.get_variation_data(product_id=product_id)    
    return JsonResponse({'data':variation_list_data})


def product_images(request, product_id=None):
    """
    Take product's id, and get all its variations.
    """
    images_list_data = ProductImage.objects.get_images_data(product_id=product_id)    
    return JsonResponse({'data':images_list_data})


def add_review(request):
    """
    Add review.
    """
    # get review by its id.
    product_id = request.POST.get("product_id")
    rate_value = int(request.POST.get("rate"))
    review_form = AddReviewForm(request.POST or None) 
    data = dict()
    if request.method == "POST":
        if review_form.is_valid():
            # create new review
            review_title = review_form.cleaned_data.get("title")
            review_content = review_form.cleaned_data.get("content")
            user_product_review = ProductReview.objects.create(user=request.user, product_id=product_id, rate=rate_value, title=review_title, content=review_content)
            data['form_is_valid'] = True
            data['success_message'] = "Your review was added successfully."
            # get product's reviews
            product_reviews = ProductReview.objects.filter(product__id=product_id)
            # get product average rate
            data['html_reviews_avg_rate'] = get_product_reviews_avg_rate(product_reviews)['html_reviews_avg_rate']
            context = {"is_review_allowed":True, "is_review_exists":True, 'reviews':product_reviews, 'user_product_review':user_product_review}
            data['html_reviews_list'] = render_to_string('product/includes/partial_product_reviews_list.html', context, request=request)
    return JsonResponse(data)


def product_user_rate(request):
    """
    Take product's id, and get its user's review rate.
    """
    product_id = request.GET.get("product_id")
    # get user's review for this product
    review = ProductReview.objects.filter(user=request.user, product__id=product_id).first()    
    return JsonResponse({'rate':review.rate})


def update_review(request):
    """
    Update review.
    """
    data = dict()
    if request.method == "POST":
        product_id = request.POST.get("product_id")
        rate_value = int(request.POST.get("rate"))
        review = ProductReview.objects.filter(user=request.user, product__id=product_id).first()
        review_form = AddReviewForm(request.POST, instance=review)
        if review_form.is_valid():
            # update review
            user_product_review = review_form.save()
            user_product_review.rate = rate_value
            user_product_review.save()
            data['form_is_valid'] = True
            data['success_message'] = "Your review was updated successfully."
            # get product's reviews
            product_reviews = ProductReview.objects.filter(product__id=product_id)
            # get product average rate
            data['html_reviews_avg_rate'] = get_product_reviews_avg_rate(product_reviews)['html_reviews_avg_rate']
            context = {"is_review_allowed":True, "is_review_exists":True, 'reviews':product_reviews, 'user_product_review':user_product_review}
            data['html_reviews_list'] = render_to_string('product/includes/partial_product_reviews_list.html', context, request=request)
    else:
        review = get_object_or_404(ProductReview, pk=request.GET.get("review_id"))
        review_form = AddReviewForm(instance=review)
        context = {"is_review_exists":False, 'form':review_form, 'is_updated':True}
        data['html_form'] = render_to_string('product/includes/partial_product_user_review.html', context, request=request)
    return JsonResponse(data)


def delete_review(request):
    """
    Delete review.
    """
    data = dict()
    if request.method == "POST":
        product_id = request.POST.get("product_id")
        review = ProductReview.objects.filter(user=request.user, product__id=product_id).first()
        # delete review.
        review.delete()
        data['form_is_valid'] = True
        data['success_message'] = "Your review was deleted successfully."
        # get product's reviews
        product_id = request.POST.get("product_id")
        product_reviews = ProductReview.objects.filter(product__id=product_id)
        review_form = AddReviewForm()
        # get product average rate
        data['html_reviews_avg_rate'] = get_product_reviews_avg_rate(product_reviews)['html_reviews_avg_rate']
        context = {"is_review_allowed":True, "is_review_exists":False, 'reviews':product_reviews, 'form':review_form}
        data['html_reviews_list'] = render_to_string('product/includes/partial_product_reviews_list.html', context, request=request)
    else:
        review = ProductReview.objects.filter(user=request.user, product__id=request.GET.get("product_id")).first()
        data['html_form'] = render_to_string('product/includes/partial_product_delete_review_form.html', {'review':review}, request=request)    
    return JsonResponse(data)    