from django.urls import path, re_path

from .views import category_list 

# namespace = category 

urlpatterns = [
    # path('<str:category_slug>/', category_list, name='category-list'),
    re_path(r'^(?P<category_slug>(.*))/$', category_list, name='category-list'),
]