from django.test import TestCase, Client
from products.models import *
from products.views import *
from django.urls import reverse
from django.db.models.query import QuerySet
from django.core.paginator import Page
from django.core.cache import cache

class HomeViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('home')
        self.category = Category.objects.create(name = 'test category')
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.type_flavor = TypeFlavor.objects.create(name = "flavor")
        for i in range(32):
            product = Product.objects.create(
                name = f'Test product {i}',
                description = f'Test description {i}',
                price = 100,
                category = self.category,
                quantity = 10,
                volume = '100ml',
                available = True,
                image = 'test.png'
            )
            product.type_flavor.add(self.type_flavor)

        self.response = self.client.get(self.url)
        cache.clear()
    
    def test_template_use(self):
        self.assertTemplateUsed(self.response, 'home.html')
    
    def test_status_code(self):
        self.assertEqual(self.response.status_code, 200)
    
    def test_context(self):
        self.assertIn('products', self.response.context)
        self.assertIn('page_products', self.response.context)
        self.assertIn('filter', self.response.context)
        self.assertIn('cart_products', self.response.context)
        self.assertIn('cart', self.response.context)
        self.assertIn('categories', self.response.context)
        self.assertIn('flavors', self.response.context)
    
    def test_context_isinctance(self):
        self.assertIsInstance(self.response.context['products'], QuerySet)
        self.assertIsInstance(self.response.context['page_products'], Page)
        self.assertIsInstance(self.response.context['filter'], ProductFilter)
        self.assertIsInstance(self.response.context['cart_products'], set)
    
    def test_products_pagination(self):
        self.assertEqual(len(self.response.context['page_products']), 16)
        response = self.client.get(self.url + '?page=2')
        self.assertEqual(len(response.context['page_products']), 16)

class DetailProductViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(name = 'test category')
        self.type_flavor = TypeFlavor.objects.create(name = "flavor")
        self.product = Product.objects.create(
            name = f'Product',
            description = f'Test description ',
            price = 100,
            category = self.category,
            quantity = 10,
            volume = '100ml',
            available = True,
            image = 'test.png',
            views = 0,
            slug='test-product'
        )
        self.product.type_flavor.add(self.type_flavor)
        self.url = reverse('detail_product', kwargs = {'slug':self.product.slug})
        self.response = self.client.get(self.url)
        cache.clear()

    def test_template_use(self):
        self.assertTemplateUsed(self.response, 'detail_product.html')
    
    def test_status_code(self):
        self.assertEqual(self.response.status_code, 200)
    
    def test_increment_product_view(self):
        initial_view = self.product.views
        self.product.refresh_from_db()
        self.assertEqual(self.product.views, initial_view + 1)

    def test_product_context(self):
        self.assertIn('product', self.response.context)
        self.assertIn('review_form', self.response.context)
        self.assertIn('cart_products', self.response.context)
        self.assertIn('product_reviews', self.response.context)
        self.assertIn('categories', self.response.context)
        self.assertIn('flavors', self.response.context)
    
class ProductByCategoryTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.category1 = Category.objects.create(name="Test Category", slug="test-category")
        self.category2 = Category.objects.create(name="Test Category 2", slug="test-category-2")
        self.type_flavor = TypeFlavor.objects.create(name="Flavor")

        for i in range(52):
            product = Product.objects.create(
                name=f"Test product {i}",
                description="Test description",
                price=100,
                category=self.category1 if i % 2 == 0 else self.category2,
                quantity=10,
                volume="100ml",
                available=True,
                image="test.png"
            )
            product.type_flavor.add(self.type_flavor)

        self.url_category1 = reverse("product_by_category", kwargs={"slug": self.category1.slug})
        self.url_category2 = reverse("product_by_category", kwargs={"slug": self.category2.slug})

        cache.clear()

    def test_template_use(self):
        response = self.client.get(self.url_category1)
        self.assertTemplateUsed(response, "product_category.html")
    
    def test_status_code(self):
        response = self.client.get(self.url_category1)
        self.assertEqual(response.status_code, 200)

        response = self.client.get(self.url_category2)
        self.assertEqual(response.status_code, 200)

    def test_category_page_loads(self):
        response = self.client.get(self.url_category1)
        self.assertEqual(response.context["category"], self.category1)

    def test_product_filtering(self):
        response = self.client.get(self.url_category1)

        products = response.context["page_products"]
        for product in products:
            self.assertEqual(product.category, self.category1)

        response = self.client.get(self.url_category2)

        products = response.context["page_products"]
        for product in products:
            self.assertEqual(product.category, self.category2)

    def test_pagination(self):
        response = self.client.get(self.url_category1)
        self.assertEqual(len(response.context["page_products"]), 16)

        response = self.client.get(self.url_category1 + "?page=2")
        self.assertEqual(len(response.context["page_products"]), 10)

        response = self.client.get(self.url_category2)
        self.assertEqual(len(response.context["page_products"]), 16)

        response = self.client.get(self.url_category2 + '?page=2')
        self.assertEqual(len(response.context["page_products"]), 10)
    
    def test_product_category_context(self):
        response = self.client.get(self.url_category1)
        self.assertIn('category', response.context)
        self.assertIn('products', response.context)
        self.assertIn('page_products', response.context)
        self.assertIn('filter', response.context)
        self.assertIn('cart_products', response.context)
        self.assertIn('cart', response.context)
        self.assertIn('categories', response.context)
        self.assertIn('flavors', response.context)


class ProductByFlavorTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(name="Test Category")
        self.type_flavor1 = TypeFlavor.objects.create(name="Flavor1")
        self.type_flavor2 = TypeFlavor.objects.create(name="Flavor2")

        for i in range(52):
            product = Product.objects.create(
                name=f"Test product {i}",
                description="Test description",
                price=100,
                category=self.category,
                quantity=10,
                volume="100ml",
                available=True,
                image="test.png"
            )
            flavor = self.type_flavor1 if i % 2 == 0 else self.type_flavor2
            product.type_flavor.add(flavor)
            product.save()
            product.refresh_from_db()

        self.url_flavor1 = reverse("product_by_flavor", kwargs={"slug": self.type_flavor1.slug})
        self.url_flavor2 = reverse("product_by_flavor", kwargs={"slug": self.type_flavor2.slug})

        cache.clear()

    def test_template_use(self):
        response = self.client.get(self.url_flavor1)
        self.assertTemplateUsed(response, "product_flavor.html")
    
    def test_status_code(self):
        response = self.client.get(self.url_flavor1)
        self.assertEqual(response.status_code, 200)

        response = self.client.get(self.url_flavor2)
        self.assertEqual(response.status_code, 200)

    def test_category_page_loads(self):
        response = self.client.get(self.url_flavor1)
        self.assertEqual(response.context["flavor"], self.type_flavor1)

        response = self.client.get(self.url_flavor2)
        self.assertEqual(response.context["flavor"], self.type_flavor2)

    def test_pagination(self):
        response = self.client.get(self.url_flavor1)
        self.assertEqual(len(response.context["page_products"]), 16)

        response = self.client.get(self.url_flavor1 + "?page=2")
        self.assertEqual(len(response.context["page_products"]), 10)

        response = self.client.get(self.url_flavor2)
        self.assertEqual(len(response.context["page_products"]), 16)

        response = self.client.get(self.url_flavor2 + '?page=2')
        self.assertEqual(len(response.context["page_products"]), 10)
    
    def test_product_category_context(self):
        response = self.client.get(self.url_flavor1)
        self.assertIn('flavor', response.context)
        self.assertIn('products', response.context)
        self.assertIn('page_products', response.context)
        self.assertIn('filter', response.context)
        self.assertIn('cart_products', response.context)
        self.assertIn('cart', response.context)
        self.assertIn('categories', response.context)
        self.assertIn('flavors', response.context)
    
class SearchViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(name="Test Category")
        self.type_flavor = TypeFlavor.objects.create(name="Flavor")

        for i in range(52):
            product = Product.objects.create(
                name=f"Test product {i}",
                description="Test description",
                price= 100 if i % 2 == 0 else 500,
                category=self.category,
                quantity=10,
                volume="100ml",
                available=True,
                image="test.png"
            )
            product.type_flavor.add(self.type_flavor)

        self.url = reverse('search')
        self.response = self.client.get(self.url)

    def test_template_use(self):
        self.assertTemplateUsed(self.response, 'search.html')
    
    def test_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_search_by_name(self):
        response = self.client.get(self.url, {'query': 'Test product 1'})
        self.assertEqual(response.status_code, 200)
        products = response.context['page_products']
        self.assertTrue(any("Test product 1" in product.name for product in products))
    
    def test_search_by_category(self):
        response = self.client.get(self.url, {'query': 'Test Category'})
        self.assertEqual(response.status_code, 200)
        products = response.context['page_products']
        self.assertGreater(len(products), 0)
    
    def test_search_by_flavor(self):
        response = self.client.get(self.url, {'query': 'Flavor'})
        self.assertEqual(response.status_code, 200)
        products = response.context['page_products']
        for product in products:
            self.assertTrue(product.type_flavor.filter(name = 'Flavor').exists())
    
    def test_products_pagination(self):
        response = self.client.get(self.url, {'query': 'Test', 'page':1})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['page_products']), 16)
        response = self.client.get(self.url, {'query': 'Test', 'page':2})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['page_products']), 16)

    def test_search_products_by_price(self):
        response = self.client.get(self.url, {'min_price': 200, 'max_price':600})
        self.assertEqual(response.status_code, 200)
        products = response.context['page_products']
        for product in products:
            self.assertTrue(200 <= product.price <= 600)
        
    def test_search_view_context(self):
        self.assertIn('search_form', self.response.context)
        self.assertIn('result', self.response.context)
        self.assertIn('page_products', self.response.context)
        self.assertIn('filter', self.response.context)
        self.assertIn('cart_products', self.response.context)
        self.assertIn('cart', self.response.context)
