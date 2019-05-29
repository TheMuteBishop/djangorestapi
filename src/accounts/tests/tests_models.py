from django.test import TestCase

from django.contrib.auth import get_user_model


class ModelTests(TestCase):

    def test_create_user_with_email(self):
        """ Create new user with given email and password """
        email = 'user@example.com'
        password = 'TestPassword123'

        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email, msg='Email did not match')
        self.assertTrue(
            user.check_password(password),
            msg='incorrect password'
        )

    def test_normalized_email(self):
        """ make email doamain lowercase """
        email = 'user@EXAMPLE.com'
        password = 'TestPassword123'

        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email.lower(), msg='Email did not match')

    def test_new_user_email_required(self):
        """ test new user with no email raises error """

        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'TestPassword123')

    def test_create_superuser_with_email(self):
        """ Create new superuseruser with given email and password """
        email = 'user@example.com'
        password = 'TestPassword123'

        user = get_user_model().objects.create_superuser(
            email=email,
            password=password
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
