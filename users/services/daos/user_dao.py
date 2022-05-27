from .base_dao import BaseDAO
from app.models import User

class UserDAO(BaseDAO):
    MODEL_CLASS = User

    def get_admin(self) -> User:
        return User.objects.filter(username='admin').first()