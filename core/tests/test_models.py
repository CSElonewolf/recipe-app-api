from django.test import TestCase
from django.contrib.auth import get_user_model

class ModelTests(TestCase):
	def test_create_user_with_email(self):
		"""Test if the user with email as username is created or not """

		email = 'exmaple@gmail.com'
		password = 'testpassword@123'

		user = get_user_model().objects.create_user(email = email,password=password
		)

		self.assertEqual(user.email,email)
		self.assertTrue(user.check_password(password))

	def test_new_user_email_normalized(self):
		"""Test if the email for a new user is normalized or not """
		email = 'test@EXAMPLE.COM'

		user = get_user_model().objects.create_user(email,'test@password123')

		self.assertEqual(user.email, email.lower())

	def test_new_user_invalid_email(self):
		"""Test creating user with no email raises error"""
		with self.assertRaises(ValueError):
			get_user_model().objects.create_user(None,'test123')

	def test_create_superuser(self):
		"""Tests whether superuser can be created or not """
		user = get_user_model().objects.create_superuser(
			email = 'test@example.com',
			password = 'testpassword@123'
		)

		self.assertTrue(user.is_staff)
		self.assertTrue(user.is_superuser)

