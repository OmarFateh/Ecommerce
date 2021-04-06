from django.urls import path

from .views import index

# namespace = home

urlpatterns = [
    path('', index, name='index'),
]