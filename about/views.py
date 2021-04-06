from django.shortcuts import render


def about(request):
    """
    Display about page.
    """
    return render(request, 'about/about.html', {})