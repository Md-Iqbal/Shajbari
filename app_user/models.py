from django.db import models
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(blank=True, max_length=20)
    zipcode = models.TextField(blank=True, null=True, max_length=10)
    address = models.TextField(blank=True, max_length=200)
    city = models.CharField(blank=True, max_length=20)
    country = models.CharField(blank=True, max_length=20)
    image = models.ImageField(blank=True, null=True, upload_to='users_img/', default='users_img/default/default.jpg')
    email_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
    
    
    def user_name(self):
        return self.user.first_name+' '+self.user.last_name+' ['+self.user.username+']'

    def image_tag(self):
        return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))
    image_tag.short_description = 'Image'


# @receiver(post_save, sender=User)
# def update_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)
#     instance.profile.save()
