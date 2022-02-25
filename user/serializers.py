from django.contrib.auth import get_user_model,authenticate
from rest_framework import serializers
from django.utils.translation import ugettext_lazy as _

class UserSerializer(serializers.ModelSerializer):
	"""Serializer for the users object """

	class Meta:
		model = get_user_model()
		fields =  ('email','password','name')
		extra_kwargs = {'password':{
			'write_only': True,
			'style':{
					'input_type':'password',
				},
			'min_length':5 }}

	def create(self,validated_data):
		"""Create a new user with encrypted password and return it """
		return get_user_model().objects.create_user(**validated_data)

	def update(self,instance,validated_data):
		"""Udate an user , setting th epassword correctly and return it """
		password = validated_data.pop('password',None)
		user = super().update(instance,validated_data)


		if password:
			user.set_password(password)
			user.save()

		return user


class AuthTokenSerializer(serializers.Serializer):
	"""Serializer for the user authentication object"""
	email = serializers.CharField()
	password = serializers.CharField(
		style={'input_type':'password'},
		trim_whitespace=False
	)

	def validate(self,attrs):
		"""Validate and authenticate the user"""
		email = attrs.get('email')
		password = attrs.get('password')


		user = authenticate(
			request =self.context.get('request'),
			email = email,
			password = password
		)

		if not user:
			msg = ('Unable to authenicate with provided credentials')
			raise serializers.ValidationError(msg,code='authentication')

		attrs['user'] = user
		return attrs
