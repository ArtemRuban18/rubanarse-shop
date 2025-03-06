from orders.models import Order, OrderProduct
from products.models import Product, TypeFlavor, Category
from django.test import TestCase
from django.contrib.auth.models import User


class OrderTest(TestCase):
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

        self.order = Order.objects.create(
            order_id = 9432,
            user = self.user,
            full_name = "Yarmola",
            phone = "**********",
            email = 'some@gmail.com',
            comment = "Some",
        )

        self.order_product1 = OrderProduct.objects.create(
            order = self.order,
            product = self.product,
            quantity = 3,
        )
        self.order_product2 = OrderProduct.objects.create(
            order = self.order,
            product = self.product2,
            quantity = 2,
        )

    def test_order_create(self):
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(self.order.order_id, 9432)
        self.assertEqual(self.order.user, self.user)
        self.assertEqual(self.order.full_name, "Yarmola")
        self.assertEqual(self.order.phone, "**********")
        self.assertEqual(self.order.email, "some@gmail.com")
        self.assertEqual(self.order.comment, "Some")
        self.assertTrue(self.order.created_at)
        self.assertEqual(self.order.payment_method, 'upon receipt')
        self.assertEqual(self.order.status, 'created')
    
    def test_order_isinctance(self):
        self.assertIsInstance(self.order, Order)
    
    def test_order_str(self):
        self.assertEqual(str(self.order), f"{self.order.order_id}")
    
    def test_confirm_order(self):
        self.order.confirm_order()
        self.assertEqual(self.order.status, 'confirmed')

        self.product.refresh_from_db()
        self.product2.refresh_from_db()
        self.assertEqual(self.product.quantity, 7)
        self.assertEqual(self.product2.quantity, 8)

    def test_cancel_order(self):
        self.order.status = 'created'
        self.order.save()
        self.order.cancel_order()
        self.assertEqual(self.order.status, 'cancelled')
    
    def test_order_total_price(self):
        self.assertEqual(self.order.total_price(), 800)

class OrderProductTest(TestCase):
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

        self.order = Order.objects.create(
            order_id = 9432,
            user = self.user,
            full_name = "Yarmola",
            phone = "**********",
            email = 'some@gmail.com',
            comment = "Some",
        )

        self.order_product = OrderProduct.objects.create(
            order = self.order,
            product = self.product,
            quantity = 3,
        )

    def test_order_product_create(self):
        self.assertEqual(OrderProduct.objects.count(), 1)
        self.assertEqual(self.order_product.order, self.order)
        self.assertEqual(self.order_product.product, self.product)
        self.assertEqual(self.order_product.quantity, 3)
    
    def test_order_product_isinctance(self):
        self.assertIsInstance(self.order_product, OrderProduct)

    def test_total_price_order_product(self):
        self.assertEqual(self.order_product.total_price(), 600)

    def test_order_product_str(self):
        self.assertEqual(str(self.order_product), f'{self.order_product.product} - {self.order_product.quantity}')

    def test_change_product_quantity_in_order(self):
        self.order_product.quantity = 10
        self.order_product.save()
        self.order.confirm_order()
        self.product.refresh_from_db()
        self.assertEqual(self.order_product.total_price(), 2000)
        self.assertEqual(self.product.quantity, 0)