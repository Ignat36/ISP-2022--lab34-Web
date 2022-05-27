from .base_dao import BaseDAO
from users.models import Profile

class ProfileDAO(BaseDAO):
    MODEL_CLASS = Profile