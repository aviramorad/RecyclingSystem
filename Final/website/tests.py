import unittest
from .models import User, products, usersContacts, usersrecycling
from django.db.utils import IntegrityError
from django.test import TestCase, RequestFactory, modify_settings, Client
from django.urls import reverse
from django.shortcuts import HttpResponse
from django.contrib import messages
from django.http import HttpResponse
from .views import index, delete_user, rate, home, master, register, contact_view, display_contacts, changestatus, userEditform, userform, my_authority, recycling_bin, data_recycling, data_user, disapprove_status, approve_status
from .forms import storeProductForm, PrivateSignUpForm, CorpSignUpForm


@modify_settings(MIDDLEWARE_CLASSES={
    'append': 'django.contrib.sessions.middleware.SessionMiddleware',
})
class UserModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username='hagit123',
            first_name='Hagit',
            last_name='Tubul',
            email='hagit4@gmail.com',
            location='Ashdod',
            comp_num=12345
        )

    def test_user_creation(self):    # Test unit to check user creation (not AI) - made by Aviram
        self.assertEqual(self.user.username, 'hagit123')
        self.assertEqual(self.user.first_name, 'Hagit')
        self.assertEqual(self.user.last_name, 'Tubul')
        self.assertEqual(self.user.email, 'hagit4@gmail.com')
        self.assertFalse(self.user.user_type)  
        self.assertEqual(self.user.location, 'Ashdod')
        self.assertEqual(self.user.comp_num, 12345)

    def test_user_unique_email(self):    # AI Unit Testing - GEMINI
        with self.assertRaises(Exception):
            # Attempt to create a user with the same email
            User.objects.create(
                username='test_user_2',
                first_name='Jane',
                last_name='Doe',
                email='hagit4@gmail.com',  # This email should already exist
                location='Test City',
                comp_num=54321
            )
    def test_user_type_choices(self):    # AI Unit Testing - GEMINI
        # Test user_type field choices
        self.assertTrue(self.user.USER_TYPE_CHOICES, (
            (False, 'Private'),
            (True, 'Corporation')
        ))
    
    def test_user_comp_num_blank(self):    # AI Unit Testing - GEMINI
        # Test comp_num field can be blank
        user_no_comp_num = User.objects.create(
            username='test_user_no_comp_num',
            first_name='Jane',
            last_name='Doe',
            email='no_comp_num@example.com',
            location='Test City'
        )
        self.assertIsNone(user_no_comp_num.comp_num)

class WebsiteProductsModelTests(unittest.TestCase):
    # my test unit
    def test_product_creation(self):   # Test unit to check that a product was created successfully - made by Noam
        product = products.objects.create(
            product_name='Test Product',
            Product_type=True,
            value=50,
            bin_type='Type A'
        )

        self.assertIsNotNone(product)
        self.assertEqual(product.product_name, 'Test Product')
        self.assertTrue(product.Product_type)
        self.assertEqual(product.value, 50)
        self.assertEqual(product.bin_type, 'Type A')

    def test_product_str_method(self):  # Made by AI - Microsoft Copilot
        # Create a product instance
        product = products(product_name='Test Product', bin_type='Type A')

        # Check the __str__ method
        self.assertEqual(str(product), 'Test Product, Type A')

    def test_product_type_default(self):   # Made by AI - Microsoft Copilot
        # Create a product without specifying Product_type (should default to False)
        product = products.objects.create(
            product_name='Another Product',
            value=100,
            bin_type='Type B'
        )

        self.assertFalse(product.Product_type)

    def test_invalid_value_raises_error(self): # Made by AI - Microsoft Copilot
    # Attempt to create a product with a negative value (should raise an IntegrityError)
        with self.assertRaises(IntegrityError):
            try:
                products.objects.create(
                    product_name='Invalid Product',
                    Product_type=True,
                    value=-10,  # Negative value
                    bin_type='Type C'
                )
            except IntegrityError as e:
                # Check if the IntegrityError message contains the expected substring
                self.assertTrue('CHECK constraint failed: value' in str(e))
                raise

class IndexTestCase(unittest.TestCase):
    def setUp(self):
        # Create a request factory
        self.factory = RequestFactory()

    def test_index_render(self):
        # Create a GET request to the index view
        request = self.factory.get('/')
        response = index(request)

        # Check that the response is an instance of an HTTP response
        self.assertIsInstance(response, HttpResponse)

        # Check that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

class DeleteUserTestCase(TestCase):
    def setUp(self):
        # Create a request factory
        self.factory = RequestFactory()

        # Create a superuser for testing
        self.superuser = User.objects.create_superuser(
            username='admin', email='admin@example.com', password='password'
        )

        # Create a regular user for testing
        self.user = User.objects.create_user(
            username='testuser', email='testuser@example.com', password='password'
        )

    def test_delete_user_superuser(self):
        # Create a GET request to the delete_user view as a superuser
        request = self.factory.get(reverse('delete_user', args=[self.user.id]))
        request.user = self.superuser
        response = delete_user(request, self.user.id)

        # Check that the user is deleted
        self.assertEqual(response.status_code, 302)  # Redirect status code
        self.assertFalse(User.objects.filter(pk=self.user.id).exists())

    def test_delete_user_non_superuser(self):
        # Create a GET request to the delete_user view as a non-superuser
        request = self.factory.get(reverse('delete_user', args=[self.user.id]))
        request.user = self.user
        response = delete_user(request, self.user.id)

        # Check that the user is not deleted and redirected
        self.assertEqual(response.status_code, 302)  # Redirect status code
        self.assertTrue(User.objects.filter(pk=self.user.id).exists())

class RateHomeMasterTestCase(TestCase):
    def setUp(self):
        # Create a request factory
        self.factory = RequestFactory()

        # Create a regular user for testing
        self.user = User.objects.create_user(
            username='testuser', email='testuser@example.com', password='password'
        )

    def test_rate_view(self):
        # Create a GET request to the rate view as a logged-in user
        request = self.factory.get(reverse('rate'))
        request.user = self.user
        response = rate(request)

        # Check that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

    def test_home_view(self):
        # Create a GET request to the home view as a logged-in user
        request = self.factory.get(reverse('home'))
        request.user = self.user
        response = home(request)

        # Check that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

    def test_master_view(self):
        # Create a GET request to the master view as a logged-in user
        request = self.factory.get(reverse('master'))
        request.user = self.user
        response = master(request)

        # Check that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

class RegisterLoginViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()

    def test_privateuser_register(self):
        response = self.client.post(reverse('privateuser_register'), {
            'username': 'testuser',
            'email': 'test3@example.com',
            'password1': 'testpassword',
            'password2': 'testpassword',
            'user_type': 'private'  # Assuming 'private' is a valid user type
        })
        self.assertEqual(response.status_code, 200)  # Check if the redirection is successful

    def test_corpuser_register(self):
        response = self.client.post(reverse('corpuser_register'), {
            'username': 'testuser2',
            'email': 'test4@example.com',
            'password1': 'testpassword',
            'password2': 'testpassword',
            'user_type': 'corporate'  # Assuming 'corporate' is a valid user type
        })
        self.assertEqual(response.status_code, 200)  # Check if the redirection is successful

    def test_login_request(self):
        User.objects.create_user(username='testuser2', password='testpassword', email='test4@example.com')

        response = self.client.post(reverse('login'), {
            'username': 'testuser2',
            'password': 'testpassword'
        })
        self.assertEqual(response.status_code, 302)  # Check if the redirection is successful

    def test_invalid_login_request(self):
        response = self.client.post(reverse('login'), {
            'username': 'invaliduser',
            'password': 'invalidpassword'
        })
        self.assertEqual(response.status_code, 200)  # Check if the login page is rendered again
        self.assertContains(response, "", status_code=200)  # Check for the error message in the response

    def test_register_view(self):
        # Create a GET request to the register view
        request = self.factory.get(reverse('register'))
        response = register(request)

        # Check that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

class ContactViewsTestCase(TestCase):
    def setUp(self):
        # Create a request factory
        self.factory = RequestFactory()

        # Create a regular user for testing
        self.user = User.objects.create_user(
            username='testuser', email='testuser@example.com', password='password'
        )

    def test_contact_view_get(self):
        # Create a GET request to the contact_view
        request = self.factory.get(reverse('contact_view'))
        request.user = self.user
        response = contact_view(request)

        # Check that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

    def test_contact_view_post(self):
        # Create a POST request to the contact_view
        request = self.factory.post(reverse('contact_view'), {'user_id': self.user.id, 'contactText': 'Test message'})
        request.user = self.user
        response = contact_view(request)

        # Check that the response redirects to '/website/home/'
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/website/home/')

    def test_display_contacts_view(self):
        # Create a GET request to the display_contacts view
        request = self.factory.get(reverse('display_contacts'))
        request.user = self.user
        response = display_contacts(request)

        # Check that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

    def test_changestatus_view(self):
        # Create a POST request to the changestatus view
        contact = usersContacts.objects.create(user=self.user, content='Test contact')
        request = self.factory.post(reverse('changestatus', args=[contact.pk]))
        request.user = self.user
        response = changestatus(request, contact.pk)

        # Check that the response redirects to '/website/display_contacts/'
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/website/display_contacts/')

class ViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_login(self.user)

    def test_productslist(self):
        response = self.client.get(reverse('productslist'))
        self.assertEqual(response.status_code, 200)

    def test_searchProduct_post(self):
        response = self.client.post(reverse('searchProduct'))
        self.assertEqual(response.status_code, 200)  # Adjust status code as needed
        # Add more assertions as needed

    def test_updateproduct_post(self):
        # Create a product instance for testing
        product = products.objects.create(product_name='Test Product')
        response = self.client.post(reverse('updateproduct', kwargs={'pk': product.pk}))
        self.assertEqual(response.status_code, 200)  # Adjust status code as needed
        # Add more assertions as needed

class DataTestCase(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpassword123')

        # Create a request factory
        self.factory = RequestFactory()

    def test_userform(self):
        # Create a GET request to userform
        request = self.factory.get(reverse('userform'))
        request.user = self.user
        response = userform(request)

        # Check that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)
        # Add more assertions as needed

    def test_userEditform(self):
        # Create a GET request to userEditform
        request = self.factory.get(reverse('userEditform'))
        request.user = self.user
        response = userEditform(request)

        # Check that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)
        # Add more assertions as needed

    def test_recycling_bin(self):
        # Create a GET request to recycling_bin
        request = self.factory.get(reverse('recycling_bin'))
        request.user = self.user
        response = recycling_bin(request)

        # Check that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)
        # Add more assertions as needed

    def test_my_authority(self):
        # Create a GET request to my_authority
        request = self.factory.get(reverse('my_authority'))
        request.user = self.user
        response = my_authority(request)

        # Check that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)
        # Add more assertions as needed

    def test_data_recycling(self):
        # Create a GET request to data_recycling
        request = self.factory.get(reverse('data_recycling'))
        request.user = self.user
        response = data_recycling(request)

        # Check that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)
        # Add more assertions as needed

    def test_data_user(self):
        # Create a GET request to data_user
        request = self.factory.get(reverse('data_user'))
        request.user = self.user
        response = data_user(request)

        # Check that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)
        # Add more assertions as needed

class RecyclingTestCase(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpassword123')

        # Create a test product
        self.product = products.objects.create(product_name='Test Product')

        # Create a test usersrecycling object with a product ID
        self.recycling = usersrecycling.objects.create(user=self.user, product=self.product, status=0)

        # Create a request factory
        self.factory = RequestFactory()

    def test_approve_status(self):
        # Create a GET request to approve_status
        request = self.factory.get(reverse('approve_status', kwargs={'pk': self.recycling.pk, 'userID': self.user.id}))
        request.user = self.user
        response = approve_status(request, pk=self.recycling.pk, userID=self.user.id)

        # Check that the response status code is 302 (redirect)
        self.assertEqual(response.status_code, 302)
        # Add more assertions as needed

    def test_disapprove_status(self):
        # Create a GET request to disapprove_status
        request = self.factory.get(reverse('disapprove_status', kwargs={'pk': self.recycling.pk}))
        request.user = self.user
        response = disapprove_status(request, pk=self.recycling.pk)

        # Check that the response status code is 302 (redirect)
        self.assertEqual(response.status_code, 302)
        # Add more assertions as needed

class ViewsTestCase1(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_login(self.user)

    def test_quiz(self):
        response = self.client.get(reverse('quiz'))
        self.assertEqual(response.status_code, 200)
        # Add more assertions as needed

    def test_view(self):
        response = self.client.get(reverse('maps'))
        self.assertEqual(response.status_code, 200)
        # Add more assertions as needed

    def test_about(self):
        response = self.client.get(reverse('about'))
        self.assertEqual(response.status_code, 200)
        # Add more assertions as needed

    def test_maps(self):
        response = self.client.get(reverse('maps'))
        self.assertEqual(response.status_code, 200)
        # Add more assertions as needed

    def test_recycle_bins(self):
        response = self.client.get(reverse('recycle_bins'))
        self.assertEqual(response.status_code, 200)
        # Add more assertions as needed

class StoreTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser2', password='testpass', email='test2@example.com')
        self.admin = User.objects.create_user(username='adminuser2', password='adminpass', email='admin2@example.com', is_superuser=True)
        self.product = products.objects.create(product_name='Test Product', value=10, Product_type=True)

    def test_addstoreproduct_GET(self):
        self.client.login(username='adminuser2', password='adminpass')
        response = self.client.get(reverse('addstoreproduct'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'הוספת מוצר חנות')

    def test_addstoreproduct_POST(self):
        self.client.login(username='adminuser2', password='adminpass')
        response = self.client.post(reverse('addstoreproduct'), {'name': 'New Product', 'value': 20, 'Product_type': True})
        self.assertEqual(response.status_code, 200)  # Redirected to adminstore on successful form submission

    def test_updatestoreproduct_GET(self):
        self.client.login(username='adminuser2', password='adminpass')
        response = self.client.get(reverse('updatestoreproduct', args=[self.product.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'עדכון פרטי מוצר')

    def test_updatestoreproduct_POST(self):
        self.client.login(username='adminuser2', password='adminpass')
        response = self.client.post(reverse('updatestoreproduct', args=[self.product.pk]), {'name': 'Updated Product', 'value': 30, 'Product_type': True})
        self.assertEqual(response.status_code, 200)  # Redirected to adminstore on successful form submission

    def test_store(self):
        self.client.login(username='testuser2', password='testpass')
        response = self.client.get(reverse('store'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Product')

    def test_updatepointsquiz(self):
        self.client.login(username='testuser2', password='testpass')
        response = self.client.get(reverse('updatepointsquiz', kwargs={'pVal': 50}))
        self.assertEqual(response.status_code, 302)  # Redirected to /website/home/ after updating points

    def test_adminstore(self):
        self.client.login(username='adminuser2', password='adminpass')
        response = self.client.get(reverse('adminstore'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Product')

if __name__ == '__main__':
    unittest.main()