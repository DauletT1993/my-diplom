from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend

class EmailAthBackend(BaseBackend):
    '''Авторизация по E-mail'''
    def authenticate(self, request, username=None, password=None, **kwargs):
        user_model = get_user_model() # Получаю модель пользователя
        try:
            user = user_model.objects.get(email=username) # Буду использовать username как email
            if user.check_password(password):# Если всё совпадает, вернётся объект user
                return user
            return None
        except (user_model.DoesNotExist, user_model.MultipleObjectsReturned):
            return None # А иначе вернётся None

    def get_user(self, user_id):
        user_model = get_user_model()  # Получаю модель пользователя
        try:
            return user_model.objects.get(pk=user_id) # Возвращаю пользователя по id
        except user_model.DoesNotExist:
            return None
