from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.conf import settings
from django.http import JsonResponse, HttpResponseRedirect
from django.template.loader import render_to_string
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required

from order.models import Order
from product.models import Product, ProductReview
from product.forms import AddReviewForm
from .forms import AddUserForm, UpdateUserForm
from .decorators import unauthenticated_user
from .utils import redirect_after_login

User = get_user_model()

# Restrict the authenticated user from visiting this page and redirect to home page.
@unauthenticated_user
def login_user(request):
    """
    Take request and login user.
    """
    url_path = request
    if request.method == "POST":
        # fetch submitted data.
        email = request.POST.get("email")
        password = request.POST.get("password")
        # check if the entered email and password are correct.
        user = authenticate(username=email, password=password)
        # Email and Password are correct. 
        if user:
            # login user.
            login(request, user)
            return redirect_after_login(url_path)
        # Email or Password is incorrect. 
        else:
            # Display error message.
            messages.error(request, 'Email or Password is incorrect.', extra_tags='login')
    return render(request, 'accounts/login.html', {})


@unauthenticated_user
def register(request):
    """
    Take request and create new account for a user.
    """
    user_form = AddUserForm(request.POST or None)
    if request.method == "POST":
        if user_form.is_valid():
            # create new user.
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data.get("password"))
            new_user.save()
            # redirect to login page and display success message.
            messages.success(request, f'Your Account has been created successfully.', extra_tags='register')
            return redirect('accounts:login')
    return render(request, 'accounts/register.html', {"form":user_form})    


def login_register_user(request):
    """
    Asynchronous login and register new users via ajax. 
    """
    data = dict()
    if request.method == "POST":
        if request.POST.get('action') == 'login':
            # fetch submitted data.
            email = request.POST.get("email")
            password = request.POST.get("password")
            # check if the entered email and password are correct.
            user = authenticate(username=email, password=password)
            # Email and Password are correct. 
            if user:
                data['form_is_valid'] = True
                # login user.
                login(request, user)
            # Email or Password is incorrect. 
            else:
                data['form_is_valid'] = False
                data['error_message'] = 'Email or Password is incorrect.'
        elif request.POST.get('action') == 'register':
            user_form = AddUserForm(request.POST)
            if user_form.is_valid():
                # create new user.
                new_user = user_form.save(commit=False)
                new_user.set_password(user_form.cleaned_data.get("password"))
                new_user.save()
                # login new user.
                login(request, new_user)
                data['form_is_valid'] = True        
    else:
        user_form = AddUserForm()
        data['html_form'] = render_to_string('accounts/includes/partial_login_form.html', {'form':user_form}, request=request)
    return JsonResponse(data)    


def validate_email(request):
    """
    Validate email asynchronously by ajax, and check if it's already been taken or not while registering or updating user.
    """
    # get submitted email.
    email = request.GET.get('email', None)
    if request.user.is_authenticated:
        # check if an account with this email already exists, in case of updating user's profile.
        is_email_taken = User.objects.filter(email__iexact=email).exclude(email__iexact=request.user.email).exists()
    else:    
        # check if an account with this email already exists, in case of registering new user.
        is_email_taken = User.objects.filter(email__iexact=email).exists()   
    data = {'is_email_taken':is_email_taken}
    if data['is_email_taken']:
        data['error_message'] = 'An account with this Email already exists.'
    return JsonResponse(data)


def logout_user(request):
    """
    Take request and logout user and delete his all session data except cart data.
    """
    for key in list(request.session.keys()):
        if key != settings.CART_SESSION_ID:
            del request.session[key]
    return redirect('/') 


@login_required
def profile(request):
    """
    Display user's data, order, favourites list, and reviews.
    Update user's profile.
    """
    # get current user
    user = get_object_or_404(User, pk=request.user.id)
    # update user's profile data
    data = dict()
    user_form = UpdateUserForm(request.POST or None, request=request, instance=user)
    if request.method == 'POST':
        if user_form.is_valid():
            data['form_is_valid'] = True
            user_form.save()
            # Display success message.
            data['success_message'] = "Your profile was updated successfully."
            data['html_form'] = render_to_string('accounts/includes/partial_profile_form.html', {'form': user_form}, request=request)
            return JsonResponse(data)     
    # get user's orders.
    orders = Order.objects.user_orders(user.id)
    # get user's reviews.
    reviews = user.reviews.all()
    # get user's favourite list.
    favourites_list = user.favourites.all()
    context = {'form':user_form, 'orders':orders, 'reviews':reviews, 'favourites_list':favourites_list}
    return render(request, 'accounts/profile.html', context)


@login_required
def add_delete_favourite(request):
    """
    Add and delete item to favourites list.
    """
    user = request.user
    product_id = request.POST.get("product_id")
    product = get_object_or_404(Product, pk=product_id)
    data = dict()
    # toggle favourite.
    if request.POST.get('action') == 'add':
        if product.favourites.filter(id=user.id).exists():
            product.favourites.remove(user)
            liked = False
        else:    
            product.favourites.add(user)
            liked = True
        data['liked'] = liked    
    # delete favourite.
    elif request.POST.get('action') == 'delete':
        product.favourites.remove(user)
        # get user's favourite list.
        favourites_list = user.favourites.all()
        data['html_list_data'] = render_to_string('accounts/includes/partial_wishlist.html', {'favourites_list':favourites_list})
    data['wishlist_count'] = user.favourites.count()
    return JsonResponse(data)
    

@login_required
def update_delete_review(request, review_id=None):
    """
    Take review's id, update and delete this review.
    """
    # get review by its id.
    review = get_object_or_404(ProductReview, pk=review_id)
    data = dict()
    if request.method == "POST":
        if request.POST.get('action') == 'delete':
            # delete review.
            review.delete()
            data['form_is_valid'] = True
            data['success_message'] = "Your review was deleted successfully."
        elif request.POST.get('action') == 'update': 
            # update review
            rate_value = int(request.POST.get("rate"))
            review_form = AddReviewForm(request.POST, instance=review)
            if review_form.is_valid():
                user_product_review = review_form.save()
                user_product_review.rate = rate_value
                user_product_review.save()
                data['form_is_valid'] = True
                data['success_message'] = "Your review was updated successfully." 
        # get user's reviews list
        reviews = request.user.reviews.all()
        data['html_reviews_list'] = render_to_string('accounts/includes/partial_reviews_list.html', {'reviews':reviews}, request=request)
    else:
        if request.GET.get('action') == 'delete':
            data['html_form'] = render_to_string('accounts/includes/partial_delete_review_form.html', {'review':review}, request=request)
        elif request.GET.get('action') == 'update':
            review_form = AddReviewForm(instance=review)
            data['html_form'] = render_to_string('accounts/includes/partial_update_review_form.html', {'form':review_form}, request=request) 
    return JsonResponse(data)