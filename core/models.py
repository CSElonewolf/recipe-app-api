from locale import normalize
from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,PermissionsMixin


class UserManager(BaseUserManager):
	"""Creates and saves a new user"""
	def create_user(self,email,password,**extras):
		if not email:
			raise ValueError("Users must have an email address")
		user = self.model(
			email = self.normalize_email(email),
			**extras
		)
		user.set_password(password)
		user.save(using=self._db)
		return user
	def create_superuser(self,email,password=None):

		user = self.create_user(email,password)
		user.is_staff = True
		user.is_superuser = True
		user.save(using=self._db)
		return user


class User(AbstractBaseUser,PermissionsMixin):
	"""Custom user model that supports using email instead of username"""
	email = models.EmailField(max_length=255,unique=True)
	name = models.CharField(max_length=255)
	is_active =models.BooleanField(default=True)
	is_staff = models.  BooleanField(default=False)


	objects = UserManager()

	USERNAME_FIELD = 'email'
