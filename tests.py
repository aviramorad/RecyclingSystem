import unittest
from my_app.models import website_products
from django.db.utils import IntegrityError
from django.test import TestCase, RequestFactory
from django.urls import reverse
from .views import searchProduct

# test for the model- website_products
class WebsiteProductsModelTests(unittest.TestCase):
    # my test unit
    def test_product_creation(self):
        # Create a new product
        product = website_products.objects.create(
            product_name='Test Product',
            Product_type=True,
            value=50,
            bin_type='Type A'
        )

        # Check that the product was created successfully
        self.assertIsNotNone(product)
        self.assertEqual(product.product_name, 'Test Product')
        self.assertTrue(product.Product_type)
        self.assertEqual(product.value, 50)
        self.assertEqual(product.bin_type, 'Type A')

    def test_product_str_method(self):
        # Create a product instance
        product = website_products(product_name='Test Product', bin_type='Type A')

        # Check the __str__ method
        self.assertEqual(str(product), 'Test Product, Type A')

    def test_product_type_default(self):
        # Create a product without specifying Product_type (should default to False)
        product = website_products.objects.create(
            product_name='Another Product',
            value=100,
            bin_type='Type B'
        )

        self.assertFalse(product.Product_type)

    def test_invalid_value_raises_error(self):
    # Attempt to create a product with a negative value (should raise an IntegrityError)
        with self.assertRaises(IntegrityError):
            try:
                website_products.objects.create(
                    product_name='Invalid Product',
                    Product_type=True,
                    value=-10,  # Negative value
                    bin_type='Type C'
                )
            except IntegrityError as e:
                # Check if the IntegrityError message contains the expected substring
                self.assertTrue('CHECK constraint failed: value' in str(e))
                raise


if __name__ == '__main__':
    unittest.main()
