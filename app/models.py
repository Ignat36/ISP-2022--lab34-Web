from email.policy import default
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.

class Tag(models.Model):
    """Store tags with many to many relationship with NewsItem."""
    tag_name = models.CharField(max_length=100)

    class Meta:
        ordering = ['tag_name']

    def __str__(self):
        return self.tag_name

class NewsItem(models.Model):
    """Implements all required fields for storing news in data base."""
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    image = models.URLField(default='')
    url = models.URLField(default='')
    date_posted =models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default=None)
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.title  

    
    def get_absolute_url(self):
        """Return absolute url to this news page."""
        return reverse('news-detail', kwargs={'pk': self.pk})
