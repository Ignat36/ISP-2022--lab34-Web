from django.contrib import admin
from .models import NewsItem, Tag

admin.site.register(NewsItem)
admin.site.register(Tag)