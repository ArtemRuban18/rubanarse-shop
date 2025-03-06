from products.models import *
from cart.models import *
from django.urls import reverse
from django.test import TestCase, Client
from django.contrib.auth.models import User

class AddToCartView(TestCase):
    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(name = 'category')
        self.type_flavor = TypeFlavor.objects.create(name = 'flavor')
        self.user = User.objects.create_user(username= 'user', password='password')
        self.client.force_login(self.user)
        self.cart = Cart.objects.create(user = self.user)
        self.product1 = Product.objects.create(
            name = f'Test product',
            description = f'Test description',
            price = 100,
            category = self.category,
            quantity = 10,
            volume = '100ml',
            available = True,
            image = 'test.png'
        )
        self.product2 = Product.objects.create(
            name = f'Test product 2',
            description = f'Test description 2',
            price = 100,
            category = self.category,
            quantity = 10,
            volume = '100ml',
            available = True,
            image = 'test.png'
        )

        self.product1.type_flavor.add(self.type_flavor)
        self.product2.type_flavor.add(self.type_flavor)

        self.url_product1 = reverse('add_to_cart', args=[self.product1.id])
        self.url_product2 = reverse('add_to_cart', args=[self.product2.id])

    def test_add_product_to_cart(self):
        response = self.client.get(self.url_product1)
        self.assertRedirects(response, '/')

        cart_product = CartProduct.objects.get(cart = self.cart, product = self.product1)
        self.assertEqual(cart_product.quantity, 1)
        
        response2 = self.client.get(self.url_product2)
        self.assertRedirects(response2, '/')

        cart_product2 = CartProduct.objects.get(cart = self.cart, product = self.product2)
        self.assertEqual(cart_product2.quantity, 1)

        self.assertEqual(CartProduct.objects.count(), 2)
    
    def test_status_code(self):
        response = self.client.get(self.url_product1)
        self.assertEqual(response.status_code, 302)

class DetailCartViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(name = 'category')
        self.type_flavor = TypeFlavor.objects.create(name = 'flavor')
        self.user = User.objects.create_user(username= 'user', password='password')
        self.client.force_login(self.user)
        self.cart = Cart.objects.create(user = self.user)
        self.product1 = Product.objects.create(
            name = f'Test product',
            description = f'Test description',
            price = 100,
            category = self.category,
            quantity = 10,
            volume = '100ml',
            available = True,
            image = 'test.png'
        )
        self.product2 = Product.objects.create(
            name = f'Test product 2',
            description = f'Test description 2',
            price = 100,
            category = self.category,
            quantity = 10,
            volume = '100ml',
            available = True,
            image = 'test.png'
        )

        self.product1.type_flavor.add(self.type_flavor)
        self.product2.type_flavor.add(self.type_flavor)

        self.cart_product1 = CartProduct.objects.create(cart = self.cart, product = self.product1, quantity = 2)
        self.cart_product2 = CartProduct.objects.create(cart = self.cart, product = self.product2, quantity = 4)
        self.url = reverse('detail_cart', args=[self.user.username])

    
    def test_template_use(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'detail_cart.html')
    
    def test_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def cart_total_price(self):
        self.assertEqual(self.cart.total_price(), 600)
    
    def test_view_context(self):
        response = self.client.get(self.url)
        self.assertIn('cart_products', response.context)
        self.assertIn('cart', response.context)
        self.assertIn('user', response.context)
        self.assertIn('total_price', response.context)

    def test_product_count_in_user_cart(self):
        response = self.client.get(self.url)
        self.assertEqual(self.cart.products.count(), 2)

class DeleteProductFromCartViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(name = 'category')
        self.type_flavor = TypeFlavor.objects.create(name = 'flavor')
        self.user = User.objects.create_user(username= 'user', password='password')
        self.client.force_login(self.user)
        self.cart = Cart.objects.create(user = self.user)
        self.product1 = Product.objects.create(
            name = f'Test product',
            description = f'Test description',
            price = 100,
            category = self.category,
            quantity = 10,
            volume = '100ml',
            available = True,
            image = 'test.png'
        )
        self.product2 = Product.objects.create(
            name = f'Test product 2',
            description = f'Test description 2',
            price = 100,
            category = self.category,
            quantity = 10,
            volume = '100ml',
            available = True,
            image = 'test.png'
        )

        self.product1.type_flavor.add(self.type_flavor)
        self.product2.type_flavor.add(self.type_flavor)

        CartProduct.objects.create(cart = self.cart, product = self.product1, quantity = 1)
        CartProduct.objects.create(cart = self.cart, product = self.product2, quantity = 1)

        self.url_product1 = reverse('delete_product', args=[self.product1.id])
        self.url_product2 = reverse('delete_product', args=[self.product2.id])

    def test_delete_product_to_cart(self):
        response = self.client.get(self.url_product1)
        self.assertRedirects(response, '/')

        self.assertFalse(CartProduct.objects.filter(cart=self.cart, product=self.product1).exists())
        
        response2 = self.client.get(self.url_product2)
        self.assertRedirects(response2, '/')

        self.assertFalse(CartProduct.objects.filter(cart=self.cart, product=self.product2).exists())

        self.assertEqual(CartProduct.objects.count(), 0)
    
    def test_status_code(self):
        response = self.client.get(self.url_product1)
        self.assertEqual(response.status_code, 302)