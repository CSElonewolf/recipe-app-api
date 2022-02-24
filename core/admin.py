from django.contrib import admin
#  Register your models here.
from .models import User
class UserAdmin(admin.ModelAdmin):
	readonly_fields = ('password',)
admin.site.register(User,UserAdmin)
