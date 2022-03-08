from django.test import TestCase
from unittest.mock import patch
from django.contrib.auth import get_user_model
from core import models

def sample_user(email = 'test@example.com',password = 'testpass'):
	"""Create a sample user """
	return get_user_model().objects.create_user(email,password)



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

	def test_create_new_superuser(self):
		"""Tests whether superuser can be created or not """
		user = get_user_model().objects.create_superuser(
			email = 'test@example.com',
			password = 'testpassword@123'
		)

		self.assertTrue(user.is_staff)
		self.assertTrue(user.is_superuser)


	def test_tag_str(self):
		"""Test the tag string representation """
		tag =  models.Tag.objects.create(
			user = sample_user(),
			name="Vegan"
		)

		self.assertEqual(str(tag),tag.name)

	def test_ingredient_str(self):
		"""Test the ingreient strig representation"""
		ingredient = models.Ingredient.objects.create(
			user = sample_user(),
			name='Cucumber'
		)
		self.assertEqual(str(ingredient),ingredient.name)

	def test_recipe_str(self):
		"""Test the recipe string representation"""
		recipe = models.Recipe.objects.create(
			user = sample_user(),
			title='Kichuri',
			time_minutes = 5,
			price = 5.00)

		self.assertEqual(str(recipe),recipe.title)


	@patch('uuid.uuid4')
	def test_recipe_file_name_uuid(self,mock_uuid):
		"""Test that image is saved in the correct location """
		uuid = 'test-uuid'
		mock_uuid.return_value = uuid
		file_path = models.recipe_image_file_path(None, 'myimage.jpg')

		exp_path = f'uploads/recipe/{uuid}.jpg'
		self.assertEqual(file_path,exp_path)