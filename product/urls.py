from django.urls import path

from .views import (
    product_detail, 
    product_variation, 
    product_images, 
    add_review , 
    update_review, 
    delete_review,
    product_user_rate, 
)

# namespace = product 

urlpatterns = [
    path('p/<str:product_slug>/', product_detail, name='product-detail'),
    path('ajax/p/<int:product_id>/variation/', product_variation, name='ajax-fetch-product-variation'),
    path('ajax/p/<int:product_id>/images/', product_images, name='ajax-fetch-product-images'),
    # Reviews
    path('ajax/p/review/add/', add_review, name='add-review'),
    path('ajax/p/review/update/', update_review, name='update-review'),
    path('ajax/p/review/delete/', delete_review, name='delete-review'),
    path('ajax/p/review/user/rate/', product_user_rate, name='ajax-fetch-product-user-rate'),
]
