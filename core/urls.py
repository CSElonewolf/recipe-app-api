
from django.urls import path
from . import views

urlpatterns = [
    path('', views.storeemails,name='form'),
    path('fetch/', views.fetchemails,name='fetchmail'),
    path('details/<int:pk>', views.email_details,name='email_detail'),
]
