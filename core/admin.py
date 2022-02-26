from django.contrib import admin
#  Register your models here.
from .models import User,Tag


class UserAdmin(admin.ModelAdmin):
	readonly_fields = ('password',)


admin.site.register(User,UserAdmin)
admin.site.register(Tag)
