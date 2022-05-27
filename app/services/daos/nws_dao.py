from .base_dao import BaseDAO
from app.models import NewsItem

class NewsDAO(BaseDAO):
    MODEL_CLASS = NewsItem