from django.test import Client, TestCase
from django.urls import reverse
from cart.models import *
from orders.models import *
from products.models import *
from django.contrib.auth.models import User
from django.core import mail

class CreateOrderViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='user', password='password')
        self.category = Category.objects.create(name = 'category')
        self.type_flavor = TypeFlavor.objects.create(name = 'flavor')
        self.product1 = Product.objects.create(
            name = 'Test product',
            description = 'Test description',
            price = 100,
            category = self.category,
            quantity = 10,
            volume = '100ml',
            available = True,
            image = 'test.png'
        )
        self.product2 = Product.objects.create(
            name = f'Test product 2',
            description = f'Test description',
            price = 100,
            category = self.category,
            quantity = 10,
            volume = '100ml',
            available = True,
            image = 'test.png'
        )

        self.product1.type_flavor.add(self.type_flavor)
        self.product2.type_flavor.add(self.type_flavor)
        
        self.cart = Cart.objects.create(user = self.user)
        self.cart_product1 = CartProduct.objects.create(cart = self.cart, product = self.product1, quantity = 2)
        self.cart_product2 = CartProduct.objects.create(cart = self.cart, product = self.product2, quantity = 4)

        self.url = reverse('create_order')
        self.client.login(username = 'user', password = 'password')

    def test_template_use(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'create_order.html')
    
    def test_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_not_logged_user(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
    
    def test_create_new_order(self):
        response = self.client.post(self.url, data = {
            'full_name': 'Artem Ruban',
            'phone':'************',
            'email':'some@gmail.com',
            'comment':'something',
            'payment_method':'upon receipt'})
        self.assertEqual(Order.objects.count(),1)

        order = Order.objects.first()
        self.assertEqual(order.user, self.user)
        self.assertEqual(order.products.count(), 2)
        self.assertRedirects(response, reverse('detail_order', kwargs = {'order_id':order.order_id}))
    
class DetailOrderViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='user', password='password')
        self.category = Category.objects.create(name = 'category')
        self.type_flavor = TypeFlavor.objects.create(name = 'flavor')
        self.product1 = Product.objects.create(
            name = 'Test product',
            description = 'Test description',
            price = 100,
            category = self.category,
            quantity = 10,
            volume = '100ml',
            available = True,
            image = 'test.png'
        )

        self.product1.type_flavor.add(self.type_flavor)
        
        self.order = Order.objects.create(
            order_id = 4212,
            user = self.user,
            full_name = 'some user',
            phone = '**********',
            email = 'some@gmail.com',
            payment_method = 'upon receipt',
            comment = 'something',
        )
        self.order_product = OrderProduct.objects.create(order = self.order, product = self.product1, quantity = 4)

        self.url = reverse('detail_order', args = [self.order.order_id])
        self.client.login(username = 'user', password = 'password')
    
    def test_template_use(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'detail_order.html')

    def test_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_not_logged_user(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
    
    def test_order_total_price(self):
        self.assertEqual(self.order.total_price(), 400)

class InformationAboutOrderViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='user', password='password')
        self.category = Category.objects.create(name = 'category')
        self.type_flavor = TypeFlavor.objects.create(name = 'flavor')
        self.product1 = Product.objects.create(
            name = 'Test product',
            description = 'Test description',
            price = 100,
            category = self.category,
            quantity = 10,
            volume = '100ml',
            available = True,
            image = 'test.png'
        )
        self.product2 = Product.objects.create(
            name = 'Test product 2',
            description = 'Test description 2',
            price = 100,
            category = self.category,
            quantity = 10,
            volume = '100ml',
            available = True,
            image = 'test.png'
        )

        self.product1.type_flavor.add(self.type_flavor)
        self.product2.type_flavor.add(self.type_flavor)
        
        self.order = Order.objects.create(
            order_id = 4212,
            user = self.user,
            full_name = 'some user',
            phone = '**********',
            email = 'some@gmail.com',
            payment_method = 'upon receipt',
            comment = 'something',
        )
        self.order_product1 = OrderProduct.objects.create(order = self.order, product = self.product1, quantity = 4)
        self.order_product2 = OrderProduct.objects.create(order = self.order, product = self.product2, quantity = 2)

        self.url = reverse('information_about_order', args = [self.order.order_id])
        self.client.login(username = 'user', password = 'password')

    def test_template_use(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'information_about_order.html')
    
    def test_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
    
    def test_order_context(self):
        self.assertEqual(self.order.products.count(), 2)
        self.assertEqual(self.order.total_price(), 600)
        self.assertEqual(self.order.status, 'created')
    
class ConfirmOrderViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='user', password='password')
        self.category = Category.objects.create(name = 'category')
        self.type_flavor = TypeFlavor.objects.create(name = 'flavor')
        self.cart = Cart.objects.create(user = self.user)
        self.product1 = Product.objects.create(
            name = 'Test product',
            description = 'Test description',
            price = 100,
            category = self.category,
            quantity = 10,
            volume = '100ml',
            available = True,
            image = 'test.png'
        )
        self.product2 = Product.objects.create(
            name = 'Test product 2',
            description = 'Test description 2',
            price = 100,
            category = self.category,
            quantity = 10,
            volume = '100ml',
            available = True,
            image = 'test.png'
        )
        self.product1.type_flavor.add(self.type_flavor)
        self.product2.type_flavor.add(self.type_flavor)

        self.cart_product = CartProduct.objects.create(cart = self.cart, product = self.product1, quantity = 1)
        self.cart_product2 = CartProduct.objects.create(cart = self.cart, product = self.product2, quantity = 1)
        
        self.order = Order.objects.create(
            order_id = 4212,
            user = self.user,
            full_name = 'some user',
            phone = '**********',
            email = 'some@gmail.com',
            payment_method = 'upon receipt',
            comment = 'something',
        )
        self.order_product1 = OrderProduct.objects.create(order = self.order, product = self.cart_product.product, quantity = 1)
        self.order_product2 = OrderProduct.objects.create(order = self.order, product = self.cart_product2.product, quantity = 1)

        self.url = reverse('confirm_order', args = [self.order.order_id])
        self.client.login(username = 'user', password = 'password')

    def test_template_use(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'confirm_order.html')
    
    def test_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_confirm_order(self):
        response = self.client.get(self.url)
        self.order.refresh_from_db()
        self.assertEqual(self.order.status, 'confirmed')

    def test_delete_product_from_cart(self):
        self.assertEqual(self.cart.products.count(), 2)
        response = self.client.get(self.url)
        self.order.refresh_from_db()
        self.assertEqual(self.cart.products.count(), 0)

    def test_reduce_products_in_stock(self):
        response = self.client.get(self.url)
        self.product1.refresh_from_db()
        self.product2.refresh_from_db()
        self.assertEqual(self.product1.quantity, 9)
        self.assertEqual(self.product2.quantity, 9)
    
    