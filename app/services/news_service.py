import requests
from app.models import NewsItem, Tag
from django.contrib.auth.models import User
from users.services.daos.user_dao import UserDAO
from .daos.nws_dao import NewsDAO

def update_db_with_api():
    r = requests.get('http://api.mediastack.com/v1/news?access_key=5d1ee9097b93a3a49739950f32c1fe22&countries=ru,us&languages=ru')
    result = r.json()
    data = result['data']

    us_dao: UserDAO = UserDAO()
    nw_dao: NewsDAO = NewsDAO()

    admin = us_dao.get_admin()
    for i in data:
        
        if(i['image'] == None): 
            i['image'] = ''

        if nw_dao.get_count({'title': i['title']}, {}) == 0:

            news = NewsItem(
                title=i['title'],
                description=i['description'], 
                image=i['image'], 
                url=i['url'],
                author=admin
                )

            nw_dao.save(news)