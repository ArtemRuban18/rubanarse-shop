from .models import Category, TypeFlavor

def global_context(request):
    return {
        'categories': Category.objects.all(),
        'flavors': TypeFlavor.objects.all()
    }