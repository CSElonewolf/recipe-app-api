import tempfile
import os

from PIL import Image

from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient


from core.models import Tag,Ingredient, Recipe
from recipe.serializers import RecipeSerializer,RecipeDetailSerializer

RECIPES_URL = reverse('recipe-list')


def detail_url(recipe_id):
	"""Return recipe detail URL"""
	return reverse('recipe-detail', args=(recipe_id,))

def sample_ingredient(user,name='Main ingredient'):
	"""Create an return a sample ingredient """
	return Ingredient.objects.create(user = user, name= name)

def sample_tag(user,name='Main tag'):
	"""Create an return a sample tag """
	return Tag.objects.create(user = user, name= name)

def sample_recipe(user,**params):
	"""Create and return a sample recipe"""
	defaults ={
		'title':'Sample User',
		'time_minutes':10,
		'price':5.00
	}
	defaults.update(params)

	return Recipe.objects.create(user = user, **defaults)

def image_upload_url(recipe_id):
	"""Return URl for recipe image upload """
	return reverse('recipe-upload-image',args = [recipe_id])

class PublicRecipeApiTests(TestCase) :
	"""Test unauthenticated recipe APi access"""

	def setUp(self):
		self.client = APIClient()

	def test_auth_required(self):
		"""Test that authentication is required"""
		res = self.client.get(RECIPES_URL)
		self.assertEqual(res.status_code,status.HTTP_403_FORBIDDEN)

class PrivateRecipeApiTests(TestCase):
	"""Test autheicated recipe API access"""

	def setUp(self):
		self.client = APIClient()
		self.user = get_user_model().objects.create_user('test@gmail.com','testpass')

		self.client.force_authenticate(self.user)

	def test_retrieve_recipes(self):
		"""Test retrieving a list of recipes """
		sample_recipe(user = self.user)

		res = self.client.get(RECIPES_URL)

		recipes = Recipe.objects.all().order_by('-id')
		serializer = RecipeSerializer(recipes,many=True)
		self.assertEqual(res.status_code,status.HTTP_200_OK)
		self.assertEqual(res.data,serializer.data)

	def test_recipes_limited_to_user(self):
		"""test retrieving recipes for user"""

		user2 = get_user_model().objects.create_user(
			'other@gmail.com',
			'otherpass'
		)

		sample_recipe(user = user2)
		sample_recipe(user =self.user)

		res= self.client.get(RECIPES_URL)

		recipes = Recipe.objects.filter(user = self.user)
		serializer = RecipeSerializer(recipes,many = True)
		self.assertEqual(res.status_code,status.HTTP_200_OK)
		self.assertEqual(len(res.data),1)
		self.assertEqual(res.data,serializer.data)

	def test_view_recipe_details(self):
		"""Test viewing a recip detail"""
		recipe = sample_recipe(user= self.user)
		recipe.tags.add(sample_tag(user = self.user))
		recipe.ingredients.add(sample_ingredient(user = self.user))

		url = detail_url(recipe.id)
		res = self.client.get(url)

		serializer = RecipeDetailSerializer(recipe)
		self.assertEqual(res.data , serializer.data)


class RecipeImageUploadTests(TestCase):
	"""Test recipe image uplaod feature """
	def setUp(self):
		self.client = APIClient()
		self.user = get_user_model().objects.create_user(
			'user@testserver.com',
			'testpass'
		)
		self.client.force_authenticate(self.user)
		self.recipe = sample_recipe(user = self.user)

	def tearDown(self):
		self.recipe.image.delete()

	def test_upload_image_to_recipe(self):
		"""Test uploading an email to recipe """
		url = image_upload_url(self.recipe.id)
		with tempfile.NamedTemporaryFile(suffix = '.jpg') as ntf:
			img = Image.new('RGB',(10,10))
			img.save(ntf,format = 'JPEG')
			ntf.seek(0)
			res= self.client.post(url,{'image':ntf},format = 'multipart')

		self.recipe.refresh_from_db()
		self.assertEqual(res.status_code, status.HTTP_200_OK)
		self.assertIn('image',res.data)
		self.assertTrue(os.path.exists(self.recipe.image.path))

	def test_upload_image_bad_request(self):
		"""Test uploading an invalid image """
		url = image_upload_url(self.recipe.id)
		res = self.client.post(url, {'image':'notimage'},format = 'multipart')
		self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)












