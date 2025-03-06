from django.core.exceptions import ValidationError
from products.models import Product, Category, TypeFlavor, ProductReview
from django.test import TestCase
from django.contrib.auth.models import User

class CreateCategoryTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name = "Test category")
    
    def test_object_create(self):
        self.assertEqual(Category.objects.count(), 1)

    def test_category_str(self):
        self.assertEqual(str(self.category), "Test category")
    
    def test_category_slug(self):
        self.assertEqual(self.category.slug, "test-category")
    
    def test_category_isinctance(self):
        self.assertIsInstance(self.category, Category)

    
class CreateTypeFlavorTest(TestCase):
    def setUp(self):
        self.type_flavor = TypeFlavor.objects.create(name = "Test flavor")
    
    def test_object_create(self):
        self.assertEqual(TypeFlavor.objects.count(), 1)

    def test_flavor_str(self):
        self.assertEqual(str(self.type_flavor), "Test flavor")
    
    def test_flavor_slug(self):
        self.assertEqual(self.type_flavor.slug, "test-flavor")
    
    def test_flavor_isinctance(self):
        self.assertIsInstance(self.type_flavor, TypeFlavor)
    
class CreateProductTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name = 'test category')
        self.type_flavor = TypeFlavor.objects.create(name = 'test flavor')
        self.type_flavor2 = TypeFlavor.objects.create(name = 'test flavor2')

        self.product = Product.objects.create(
            name = 'Test product',
            description = 'Test description',
            price = 100,
            category = self.category,
            quantity = 10,
            volume = '100ml',
            available = True,
            image = 'test.png'
        )
        self.product.type_flavor.add(self.type_flavor)
        self.product.type_flavor.add(self.type_flavor2)
    
    def test_product_create(self):
        self.assertEqual(Product.objects.count(), 1)
        self.assertEqual(self.product.name, 'Test product')
        self.assertEqual(self.product.description, 'Test description')
        self.assertEqual(self.product.price, 100)
        self.assertEqual(self.product.category, self.category)
        self.assertEqual(self.product.quantity, 10)
        self.assertEqual(self.product.available, True)
        self.assertEqual(self.product.image, 'test.png')
        self.assertEqual(self.product.views, 0)
        self.assertEqual(self.product.slug, 'test-product')
    
    def test_product_str(self):
        self.assertEqual(str(self.product), 'Test product')

    def test_product_negative_quantity(self):
        self.product.quantity = -10
        with self.assertRaises(ValidationError):
            self.product.full_clean()
    
    def test_product_negative_price(self):
        self.product.price = -100
        with self.assertRaises(ValidationError):
            self.product.full_clean()
    
    def test_product_isinctance(self):
        self.assertIsInstance(self.product, Product)
    
    def test_product_category(self):
        self.category2 = Category.objects.create(name = "Test category 2")
        self.product.category = self.category2
        self.product.save()
        self.assertEqual(self.product.category, self.category2)

    def test_product_list_of_type_flavor(self):
        self.assertEqual(set(self.product.type_flavor.all()), {self.type_flavor, self.type_flavor2})
    
class ProductReviewsTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name = 'category')
        self.type_flavor = TypeFlavor.objects.create(name = "flavor")
        self.product = Product.objects.create(
            name = 'Test product',
            description = 'Test description',
            price = 100,
            category = self.category,
            quantity = 10,
            volume = '100ml',
            available = True,
            image = 'test.png'
        )
        self.product.type_flavor.add(self.type_flavor)

        self.user = User.objects.create_user(username='Yarmola', password='Test password')

        self.product_review = ProductReview.objects.create(
            user = self.user,
            product = self.product,
            rating = 5,
            comment = 'some comment'
        )

    def test_product_review_create(self):
        self.assertEqual(ProductReview.objects.count(), 1)
        self.assertEqual(self.product_review.user, self.user)
        self.assertEqual(self.product_review.product, self.product)
        self.assertEqual(self.product_review.rating, 5)
        self.assertEqual(self.product_review.comment, 'some comment')
        self.assertTrue(self.product_review.created_at)
    
    def test_products_review_str(self):
        self.assertEqual(str(self.product_review), self.product.name)
    
    def test_invalid_rating(self):
        self.product_review.rating = 0
        self.product_review.save()
        with self.assertRaises(ValidationError):
            self.product_review.full_clean()

        self.product_review.rating = 6
        self.product_review.save()
        with self.assertRaises(ValidationError):
            self.product_review.full_clean()
        
    def test_blank_comment(self):
        self.product_review2 =  ProductReview.objects.create(
            user = self.user,
            product = self.product,
            rating = 4,
            comment = ''
        )

        self.assertEqual(ProductReview.objects.count(), 2)
    
    def test_isinctance(self):
        self.assertIsInstance(self.product_review, ProductReview)