from xml.parsers.expat import model
from rest_framework import serializers
from core.models import Ingredient, Tag, Recipe


class TagSerializer(serializers.ModelSerializer):
	"""serializer for tag objects"""
	class Meta:
		model = Tag
		fields = ('id','name')
		read_only_fields = ('id',)


class IngredientSerializer(serializers.ModelSerializer):
	"""Serailizers for ingredient objects"""

	class Meta:
		model = Ingredient
		fields = ('id','name',)
		read_only_fields = ('id',)

class RecipeSerializer(serializers.ModelSerializer):
	"""Serialize  a rceipe"""

	ingredients = serializers.PrimaryKeyRelatedField(many = True, queryset=Ingredient.objects.all())

	tags = serializers.PrimaryKeyRelatedField(many = True, queryset = Tag.objects.all())

	class Meta:
		model = Recipe
		fields = ('id','title','ingredients','tags','time_minutes','price','link')

		read_only_fields = ('id',)
		
class RecipeDetailSerializer(RecipeSerializer):
	"""Serializer a recipe details"""
	ingredients = IngredientSerializer(many=True,read_only = True)
	tags = TagSerializer(many= True,read_only = True)
