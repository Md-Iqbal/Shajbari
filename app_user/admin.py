from django.contrib import admin
from .models import UserProfile
# Register your models here.

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user_name', 'zipcode', 'country', 'image_tag']
    list_filter = ['country']

admin.site.register(UserProfile, UserProfileAdmin)

