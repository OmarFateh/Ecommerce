from django.urls import path

from .views import faq

# namespace = faq

urlpatterns = [
    path('faqs/', faq, name='faq'),
]