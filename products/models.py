from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length = 100, unique= True, blank = False)
    slug = models.SlugField(max_length = 100, unique = True, blank = False)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug  = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
class Product(models.Model):
    TYPE_OF_FLAVOR = {
    'floral': 'Квітковий',
    'fruity': 'Фруктовий',
    'woody': 'Деревний',
    'chypre': 'Шипровий',
    'oriental': 'Східний',
    'citrus': 'Цитрусовий',
    'spicy': 'Пряний',
    'marine': 'Морський',
    'vanilla': 'Ванільний'
}


    name = models.CharField(max_length= 255, blank = False)
    description = models.TextField(blank = False)
    price = models.DecimalField(max_digits = 10, decimal_places = 2, blank=False)
    category = models.ForeignKey(Category, on_delete = models.CASCADE, blank = False, related_name='products')
    type_of_flavor = models.CharField(choices = TYPE_OF_FLAVOR, blank = False)
    quantity = models.PositiveIntegerField(blank = False)
    image = models.ImageField(upload_to = 'images/', blank = False)
    volume = models.CharField(max_length = 100, blank = False)
    slug = models.SlugField(max_length = 255, blank = False, unique= True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name

class ProductReview(models.Model):
    CHOICES_RATING = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    )

    user = models.ForeignKey(User, on_delete = models.CASCADE)
    product = models.ForeignKey(Product, on_delete = models.CASCADE, related_name = 'product_reviews') # related_name is used to access the reviews of a product
    rating = models.PositiveIntegerField(choices = CHOICES_RATING)
    comment = models.TextField(blank = True)
    created_at = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.product.name