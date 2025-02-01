from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length = 100, unique= True, blank = False, verbose_name='Назва')
    slug = models.SlugField(max_length = 100, unique = True, blank = False)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug  = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class TypeFlavor(models.Model):
    name = models.CharField(max_length=255, blank=False, verbose_name="Аромат")
    slug = models.SlugField(max_length=255, blank=True)

    def save(self, *args,**kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length= 255, blank = False, verbose_name='Назва')
    description = models.TextField(blank = False,verbose_name='Опис')
    price = models.DecimalField(max_digits = 10, decimal_places = 2, blank=False, verbose_name='Ціна')
    category = models.ForeignKey(Category, on_delete = models.CASCADE, blank = False, related_name='products', verbose_name='Категорія')
    type_flavor = models.ManyToManyField(TypeFlavor, related_name="flavors",  verbose_name='Аромат')
    quantity = models.PositiveIntegerField(blank = False, verbose_name='Кількість')
    image = models.ImageField(upload_to = 'images/', blank = False)
    volume = models.CharField(max_length = 100, blank = False, verbose_name="Об'єм(мл)")
    slug = models.SlugField(max_length = 255, blank = False, unique= True)
    available = models.BooleanField(default=True, blank=False,  verbose_name='Доступно')
    views = models.PositiveIntegerField(default=0,  verbose_name='Кількість переглядів')
    likes = models.PositiveIntegerField(default=0, verbose_name='Кількість вподобань')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        self.available = self.quantity > 0
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

    user = models.ForeignKey(User, on_delete = models.CASCADE, verbose_name='Користувач')
    product = models.ForeignKey(Product, on_delete = models.CASCADE, related_name = 'product_reviews', verbose_name='Товар')
    rating = models.PositiveIntegerField(choices = CHOICES_RATING, verbose_name='Оцінка', blank=False)
    comment = models.TextField(blank = True, verbose_name='Коментар')
    created_at = models.DateTimeField(auto_now_add = True, verbose_name='Створено')

    def __str__(self):
        return self.product.name