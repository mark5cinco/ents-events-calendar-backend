from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

# Register your models here.
from accounts.models import User

# @admin.register(User)
# class UserAdmin(DjangoUserAdmin):
admin.site.register(User)
