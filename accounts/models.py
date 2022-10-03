from django.db import models
from django.contrib import auth
from django.contrib.auth.models import PermissionsMixin
from django.utils import timezone
# Create your models here.

class User(auth.models.User, PermissionsMixin):
    def __str__(self):
        return "@{}".format(self.username)


class UserProfileInfo(models.Model):
    # Create relationship (don't inherit from User!)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    create_time = models.DateTimeField(default=timezone.now)
    # Add any additional attributes you want
    # portfolio_site = models.URLField(blank=True)
    # pip install pillow to use this!
    # Optional: pip install pillow --global-option="build_ext" --global-option="--disable-jpeg"
    profile_pic = models.ImageField(upload_to='static/profile_img', blank=True)

    def __str__(self):
        # Built-in attribute of django.contrib.auth.models.User !
        return self.user.username