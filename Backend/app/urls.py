from django.urls import path
from .views import (
    NewsListView, 
    NewsDetailView, 
    NewsCreateView, 
    NewsUpdateView,
    NewsDeleteView,
    TagNewsListView
)
from . import views


urlpatterns = [
    path('', NewsListView.as_view(), name='news-index'),
    path('tag/<str:tag_name>', TagNewsListView.as_view(), name='news-tag'),
    path('news/<int:pk>/', NewsDetailView.as_view(), name='news-detail'),
    path('news/<int:pk>/delete/', NewsDeleteView.as_view(), name='news-delete'),
    path('news/<int:pk>/update/', NewsUpdateView.as_view(), name='news-update'),
    path('news/creation/', NewsCreateView.as_view(), name='news-create'),
    path('about/', views.about, name='news-about')
]