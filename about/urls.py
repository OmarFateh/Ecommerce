from django.urls import path

from .views import about

# namespace = about

urlpatterns = [
    path('about/', about, name='about'),
]