from django.test import TestCase
from products.models import Product, TypeFlavor, Category
from  products.filters import *

class ProductFilterTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name = 'category')

        self.type_flavor = TypeFlavor.objects.create(name= 'flavor1')
        self.type_flavor2 = TypeFlavor.objects.create(name= 'flavor2')

        self.product1 = Product.objects.create(
            name = 'product',
            description = 'description',
            price = 100,
            category = self.category,
            quantity = 100,
            image = 'image.png',
            volume = '10',
        )
        self.product2 = Product.objects.create(
            name = 'product 2',
            description = 'description 2',
            price = 600,
            category = self.category,
            quantity = 6,
            image = 'image.png',
            volume = '10',
        )
        self.product3 = Product.objects.create(
            name = 'product 3',
            description = 'description 3',
            price = 1000,
            category = self.category,
            quantity = 100,
            image = 'image.png',
            volume = '10',
        )

        self.product1.type_flavor.add(self.type_flavor, self.type_flavor2)
        self.product2.type_flavor.add(self.type_flavor)
        self.product3.type_flavor.add(self.type_flavor2)

    def test_filter_by_name(self):
        filter_data = {'name':'product'}
        filter_result = ProductFilter(filter_data, queryset=Product.objects.all()).qs
        self.assertEqual(list(filter_result), [self.product1, self.product2, self.product3])
    
    def test_filter_by_min_price(self):
        filter_data = {'price__gte': 800}
        filter_result = ProductFilter(filter_data, queryset=Product.objects.all()).qs
        self.assertEqual(list(filter_result), [self.product3])

    def test_filter_by_max_price(self):
        filter_data = {'price__lte': 800}
        filter_result = ProductFilter(filter_data, queryset=Product.objects.all()).qs
        self.assertEqual(list(filter_result), [self.product1, self.product2])

    def test_filter_by_category(self):
        filter_data = {'category': self.category}
        filter_result = ProductFilter(filter_data, queryset=Product.objects.all()).qs
        self.assertEqual(list(filter_result), [self.product1, self.product2, self.product3])
        
    def test_filter_by_type_flavor(self):
        filter_data = {'type_flavor': self.type_flavor}
        filter_result = ProductFilter(filter_data, queryset=Product.objects.all()).qs
        self.assertEqual(list(filter_result), [self.product1, self.product2])

        filter_data2 = {'type_flavor': self.type_flavor2}
        filter_result2 = ProductFilter(filter_data2, queryset=Product.objects.all()).qs
        self.assertEqual(list(filter_result2), [self.product1, self.product3])
    

