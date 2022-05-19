from django.http import HttpResponse
from django.shortcuts import render
import requests

# Create your views here.
def index(request):
    r = requests.get('http://api.mediastack.com/v1/news?access_key=07f04176b5cab9b8543438d76220d466&countries=ru,us&languages=ru')
    result = r.json()
    data = result['data']
    title = []
    description = []
    image = []
    url = []
    
    for i in data:
        title.append(i['title'])
        description.append(i['description'])
        image.append(i['image'])
        url.append(i['url'])
    
    news = zip(title, description, image, url)
    # news = [(t1,d1,i1,u1), (t2,d2,i2,u2)]

    return render(request, 'app/index.html', {'news': news})

def about(request):
    return HttpResponse('<h1>Group 053502 | Shargorodsky Ignat | Lab 3-4 </h1>News site which loads basic news from api https://mediastack.com/.<br>Site has 4 different roles Reader, Pudlisher, Edditor and Admin<br>Readers can leave comments under news.')