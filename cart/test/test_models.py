from cart.models import Cart, CartProduct
from products.models import Product, TypeFlavor, Category
from django.test import TestCase
from django.contrib.auth.models import User


class CartTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='Yarmolenko', password='testpassword')

        self.category = Category.objects.create(name = 'category')

        self.type_flavor = TypeFlavor.objects.create(name = 'test flavor')
        self.type_flavor2 = TypeFlavor.objects.create(name = 'test flavor2')

        self.product = Product.objects.create(
            name = f'Test product 1',
            description = f'Test description 1',
            price = 200,
            category = self.category,
            quantity = 10,
            volume = '100ml',
            available = True,
            image = 'test1.png'
        )

        self.product2 = Product.objects.create(
            name = f'Test product 2',
            description = f'Test description 2',
            price = 100,
            category = self.category,
            quantity = 10,
            volume = '100ml',
            available = True,
            image = 'test1.png'
        )

        self.product.type_flavor.add(self.type_flavor)
        self.product.type_flavor.add(self.type_flavor2)

        self.cart = Cart.objects.create(
            user = self.user
        )

        self.cart_product1 = CartProduct.objects.create(
            cart = self.cart,
            product = self.product,
            quantity = 3,
        )
        self.cart_product2 = CartProduct.objects.create(
            cart = self.cart,
            product = self.product2,
            quantity = 2,
        )

    def test_cart_create(self):
        self.assertEqual(Cart.objects.count(), 1)
        self.assertEqual(self.cart.user, self.user)
        self.assertTrue(self.cart.created_at)
    
    def test_cart_isinctance(self):
        self.assertIsInstance(self.cart, Cart)
    
    def test_cart_str(self):
        self.assertEqual(str(self.cart), f"Кошик {self.user}")
    
    def test_cart_total_price(self):
        self.assertEqual(self.cart.total_price(), 800)

class CartProductTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='Yarmolenko', password='testpassword')

        self.category = Category.objects.create(name = 'category')

        self.type_flavor = TypeFlavor.objects.create(name = 'test flavor')

        self.product = Product.objects.create(
            name = f'Test product 1',
            description = f'Test description 1',
            price = 200,
            category = self.category,
            quantity = 10,
            volume = '100ml',
            available = True,
            image = 'test1.png'
        )

        self.product.type_flavor.add(self.type_flavor)

        self.cart = Cart.objects.create(
            user = self.user
        )

        self.cart_product = CartProduct.objects.create(
            cart = self.cart,
            product = self.product,
            quantity = 3,
        )

    def test_cart_product_create(self):
        self.assertEqual(CartProduct.objects.count(), 1)
        self.assertEqual(self.cart_product.cart, self.cart)
        self.assertEqual(self.cart_product.product, self.product)
        self.assertEqual(self.cart_product.quantity, 3)
    
    def test_cart_product_isinctance(self):
        self.assertIsInstance(self.cart_product, CartProduct)

    def test_total_price_cart_product(self):
        self.assertEqual(self.cart_product.total_price(), 600)

    def test_cart_product_str(self):
        self.assertEqual(str(self.cart_product), f'Додано {self.cart_product.product} - {self.cart_product.quantity}')