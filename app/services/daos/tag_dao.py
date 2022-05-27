from .base_dao import BaseDAO
from app.models import Tag

class TagDAO(BaseDAO):
    MODEL_CLASS = Tag