from django.test import TestCase
import unittest
from .models import User

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

    def test_user_creation(self):    # Test unit to check user creation (not AI)
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

if __name__ == '__main__':
    unittest.main()
