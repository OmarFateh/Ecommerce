from .models import Category

def node_categories(request):
    """
    Custom context processor for node categories.
    """
    categories = Category.objects.root_nodes()
    return {'node_categories':categories,}  