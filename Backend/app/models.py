from email.policy import default
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class NewsItem(models.Model):
    """Implements all required fields for storing news in data base."""
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    image = models.URLField()
    url = models.URLField()
    date_posted =models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default=None)

    def __str__(self):
        return self.title  