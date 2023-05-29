from django.contrib import admin
from django.contrib.auth.models import User
from .models import UserProfile,Message
# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Message)
