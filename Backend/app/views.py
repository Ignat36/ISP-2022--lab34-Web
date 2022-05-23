from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (ListView, 
                                  DetailView, 
                                  CreateView,
                                  UpdateView,
                                  DeleteView
                                 )
import requests
from datetime import datetime
from app.models import NewsItem, Tag
from django.contrib.auth.models import User


class NewsListView(ListView):
    model = NewsItem
    template_name: str = 'app/index.html'
    context_object_name = 'news'
    ordering = ['-date_posted']
    paginate_by = 9


class TagNewsListView(ListView):
    model = NewsItem
    template_name: str = 'app/tag_news.html'
    context_object_name = 'news'
    ordering = ['-date_posted']
    paginate_by = 9

    def get_queryset(self):
        tag = get_object_or_404(Tag, tag_name=self.kwargs.get('tag_name'))
        return tag.newsitem_set.all()


class NewsDetailView(DetailView):
    model = NewsItem


class NewsCreateView(LoginRequiredMixin, CreateView):
    model = NewsItem
    fields = ('title', 'description', 'url', 'image', 'tags')


    def form_valid(self, form):
        form.instance.author = self.request.user

        return super().form_valid(form)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['url'].required = False
        form.fields['image'].required = False
        form.fields['tags'].required = False
        return form


class NewsUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = NewsItem
    fields = ('title', 'description', 'url', 'image', 'tags')


    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        news = self.get_object()
        if self.request.user == news.author:
            return True
        return False

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['url'].required = False
        form.fields['image'].required = False
        form.fields['tags'].required = False
        return form

class NewsDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = NewsItem
    success_url = '/'

    def test_func(self):
        news = self.get_object()
        if self.request.user == news.author:
            return True
        return False


def about(request):
    return HttpResponse('<h1>Group 053502 | Shargorodsky Ignat | Lab 3-4 </h1>News site which loads basic news from api https://mediastack.com/.<br>Site has 4 different roles Reader, Pudlisher, Edditor and Admin<br>Readers can leave comments under news.')