from django.shortcuts import render


def faq(request):
    """
    Display faq page.
    """
    return render(request, 'faq/faq.html', {})