from django.test import TestCase, Client
from django.urls import reverse

from django.contrib.auth.models import User
from app.models import NewsItem, Tag
from users.models import Profile

from app.views import *
from users.views import *

class TestProject(TestCase):
    """Class for testing project"""

    def setUp(self) -> None:
        self.tag = Tag(tag_name='name')
        self.news = NewsItem(title='title', description='description')
        self.use = User(username='user')
        self.prof = Profile(user=self.use)

        self.test_client = Client()
        self.home_url = reverse('news-index')
        self.create_url = reverse('news-create')
        self.about_url = reverse('news-about')
        self.reqister_url = reverse('register')
        self.login_url = reverse('login')
        self.logout_url = reverse('logout')
        self.profile_url = reverse('profile')

    def test_users_views_profile(self):
        respon = self.test_client.post(self.profile_url)
    
    def test_users_views_logout(self):
        respon = self.test_client.get(self.logout_url)

    def test_users_views_login(self):
        respon = self.test_client.get(self.login_url)

    def test_users_views_register(self):
        respon = self.test_client.get(self.reqister_url)

    def test_user_views_create(self):
        respon = self.test_client.get(self.create_url)

    def test_user_views_about(self):
        respon = self.test_client.get(self.about_url)

    def test_tag_str(self):
        self.assertEqual(str(self.tag), 'name')

    def test_newsitem_str(self):
        self.assertEqual(str(self.news), 'title')

    def test_profile_str(self):
        self.assertEqual(str(self.prof), 'user Profile')

    def test_profile_save(self):
        self.use.save()
        self.assertEqual(Profile.objects.filter(user=self.use).count(), 1)
        self.use.delete()
