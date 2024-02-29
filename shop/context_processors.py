from .models import Category


def categories(request):
    """
    Get the top-level categories and return them in a dictionary.
    """
    categories = Category.objects.filter(parent=None)
    return {'categories': categories}
