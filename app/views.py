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
from app.models import NewsItem, Tag
from django.contrib.auth.models import User


class NewsListView(ListView):
    """Show main page with all news stored in database."""
    model = NewsItem
    template_name: str = 'app/index.html'
    context_object_name = 'news'
    ordering = ['-date_posted']
    paginate_by = 9

    def get_queryset(self):
        """Overrided function that return query set of its models. Make request to mediastack api and add everything new to database."""
        r = requests.get('http://api.mediastack.com/v1/news?access_key=07f04176b5cab9b8543438d76220d466&countries=ru,us&languages=ru')
        result = r.json()
        data = result['data']

        # into dao
        admin = User.objects.filter(username='admin').first()
        for i in data:
            
            if(i['image'] == None): 
                i['image'] = ''

            if NewsItem.objects.filter(title=i['title']).count() == 0:
                news = NewsItem(
                    title=i['title'],
                    description=i['description'], 
                    image=i['image'], 
                    url=i['url'],
                    author=admin
                    )
                # news.save()
                # salary
                

        return super().get_queryset()
# UseCase execute all services
class TagNewsListView(ListView):
    """Show news with choosen tag."""
    model = NewsItem
    template_name: str = 'app/tag_news.html'
    context_object_name = 'news'
    paginate_by = 9

    def get_queryset(self):
        """Overrided function that return query set of its models. Return only choosen tag related objects."""
        tag = get_object_or_404(Tag, tag_name=self.kwargs.get('tag_name'))
        return tag.newsitem_set.all().order_by('-date_posted')


class NewsDetailView(DetailView):
    """Show news that have been created within this site."""
    model = NewsItem


class NewsCreateView(LoginRequiredMixin, CreateView):
    """Create news view."""
    model = NewsItem
    fields = ('title', 'description', 'url', 'image', 'tags')


    def form_valid(self, form):
        """Overrided validation """
        form.instance.author = self.request.user

        return super().form_valid(form)

    def get_form(self, form_class=None):
        """Make particular fields unrequired."""
        form = super().get_form(form_class)
        form.fields['url'].required = False
        form.fields['image'].required = False
        form.fields['tags'].required = False
        return form


class NewsUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Update news view."""
    model = NewsItem
    fields = ('title', 'description', 'url', 'image', 'tags')


    def form_valid(self, form):
        """Overrided validation """
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        """Give access if only looagged person is author."""
        news = self.get_object()
        if self.request.user == news.author:
            return True
        return False

    def get_form(self, form_class=None):
        """Make particular fields unrequired."""
        form = super().get_form(form_class)
        form.fields['url'].required = False
        form.fields['image'].required = False
        form.fields['tags'].required = False
        return form

class NewsDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Delete news view."""
    model = NewsItem
    success_url = '/'

    def test_func(self):
        """Give access if only looagged person is author."""
        news = self.get_object()
        if self.request.user == news.author:
            return True
        return False


def about(request):
    """About page :)"""
    return HttpResponse('<h1>Group 053502 | Shargorodsky Ignat | Lab 3-4 </h1>News site which loads basic news from api https://mediastack.com/.<br>Site has 4 different roles Reader, Pudlisher, Edditor and Admin<br>Readers can leave comments under news.')