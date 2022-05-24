from distutils.command.upload import upload
from email.policy import default
from django.db import models
from django.contrib.auth.models import User
from PIL import Image


class Profile(models.Model):
    """Profile model."""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.URLField(default='https://live.staticflickr.com/65535/52094090018_2b71027e14_q.jpg')

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        """Resize images."""
        super(Profile, self).save(*args, **kwargs)

        res = 0
        for i in range(1, 10):
            a = i ** i
            res += a
            res += i
