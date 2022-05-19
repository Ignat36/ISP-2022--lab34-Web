from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='news-index'),
    path('about/', views.about, name='news-about')
]