from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (ListView, 
                                  DetailView, 
                                  CreateView,
                                  UpdateView,
                                  DeleteView
                                 )
import requests
from datetime import datetime
from app.models import NewsItem

# Create your views here.
def index(request):
    r = requests.get('http://api.mediastack.com/v1/news?access_key=07f04176b5cab9b8543438d76220d466&countries=ru,us&languages=ru')
    result = r.json()
    data = result['data']
    title = []
    description = []
    image = []
    url = []
    author = []
    published_at = []

    for i in NewsItem.objects.all():
        title.append(i.title)
        description.append(i.description)
        image.append(i.image)
        url.append(i.url)
        author.append(i.author)
        url.append(i.url)
        published_at.append(i.date_posted)

    for i in data:
        title.append(i['title'])
        description.append(i['description'])
        image.append(i['image'])
        url.append(i['url'])
        author.append(i['author'])
        published_at.append(datetime.fromisoformat(i['published_at']))
    
    
    context = {
        'news': NewsItem.objects.all()
    }
    
    news = zip(title, description, image, url, author, published_at)
    # news = [(t1,d1,i1,u1), (t2,d2,i2,u2)]

    return render(request, 'app/index.html', context)


class NewsListView(ListView):
    model = NewsItem
    template_name: str = 'app/index.html'
    context_object_name = 'news'
    ordering = ['-date_posted']
    paginate_by = 9


class NewsDetailView(DetailView):
    model = NewsItem


class NewsCreateView(LoginRequiredMixin, CreateView):
    model = NewsItem
    fields = ('title', 'description', 'url', 'image')


    def form_valid(self, form):
        form.instance.author = self.request.user

        return super().form_valid(form)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['url'].required = False
        form.fields['image'].required = False
        return form


class NewsUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = NewsItem
    fields = ('title', 'description', 'url', 'image')


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