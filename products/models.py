from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class Category(models.Model):
    """
    Model for category of products

    Fieds:
        - name: name of category(CharField)
        - slug: slug of category(SlugField)    
    """

    name = models.CharField(max_length = 100, unique= True, blank = False, verbose_name='Назва')
    slug = models.SlugField(max_length = 100, unique = True, blank = False)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug  = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class TypeFlavor(models.Model):
    """
    Model for type of flavor for products
    
    Fields:
        - name: name of type flavors(CharFiled)
        - slug: slug of type flavors(SlufField)
    """

    name = models.CharField(max_length=255, blank=False, verbose_name="Аромат")
    slug = models.SlugField(max_length=255, blank=True)

    def save(self, *args,**kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name

class Product(models.Model):
    """
    Model for products

    Fields:
        - name: name of product(CharField)
        - description: description of product(TextField)
        - price: price of product(DecimalField)
        - category: category of product(ForeignKey)
        - type_flavor: type of flavor for product(ManyToManyField)
        - quantity: quantity of product(PositiveIntegerField)
        - image: image of product(ImageField)
        - volume: volume of product(CharField)
        - slug: slug of product(SlugField)
        - available: availability of product(BooleanField)
        - views: views of product(PositiveIntegerField)
    """

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

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        self.available = self.quantity > 0
        super().save(*args, **kwargs)
    
    def clean(self):
        if self.quantity < 0:
            raise ValidationError({'quantity': 'Quantity cannot be negative.'})
        if self.price < 0:
            raise ValidationError({'price': 'Price cannot be negative'})
    
    def __str__(self):
        return self.name


class ProductReview(models.Model):
    """
    Model for reviews of products
    
    Fields:
        - user: user who left a review(ForeignKey)
        - product: product for which the review was left(ForeignKey)
        - rating: rating of product(PositiveIntegerField)
        - comment: comment of user(TextField)
        - created_at: date of creation of review(DateTimeField)
    """

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

    def clean(self):
        if self.rating < 1 or self.rating > 5:
            raise ValidationError({'rating': 'Rating must be between 1 and 5.'})

    def __str__(self):
        return self.product.name