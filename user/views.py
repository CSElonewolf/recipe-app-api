from rest_framework import generics

from .serializers import UserSerializer
from core.models import User


class CreateUserView(generics.CreateAPIView):
	"""Create a new user in the system"""
	queryset = User.objects.all()
	serializer_class = UserSerializer
