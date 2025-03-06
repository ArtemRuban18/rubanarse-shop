from .models import Category, TypeFlavor

def global_context(request):
    """
    Context processor for flobal variables
    """
    return {
        'categories': Category.objects.all(),
        'flavors': TypeFlavor.objects.all()
    }