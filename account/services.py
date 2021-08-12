from django.core.cache import cache
from django.utils.datastructures import MultiValueDictKeyError

from .models import User


class UserActivityFromRequest:

    def __init__(self, request):
        self.__request = request
        self.format = '%Y-%m-%d, %H:%M:%S'

    def get_request(self):
        return self.__request

    def validate_query_parameter(self):
        try:
            request = self.get_request()
            user_id_query_parameter = request.query_params['user_id']
            return user_id_query_parameter
        except MultiValueDictKeyError as err:
            print(f'query parameter <{err}> does not include in your request')

    def get_user_id(self):
        try:
            user_id = int(self.validate_query_parameter())
            return user_id
        except (ValueError, TypeError) as err:
            print('user_id must be integer:', err)

    def get_user_last_login(self):
        user_id = self.get_user_id()
        user_exists = False
        try:
            user_last_login = User.objects.filter(id=user_id).values('last_login').first()['last_login']
            user_exists = True
            if user_last_login:
                user_last_login = user_last_login.strftime(self.format)
            return user_last_login, user_exists
        except TypeError:
            print(f'query parameters are incorrect')
            return None, user_exists

    def get_user_last_request(self):
        user_id = self.get_user_id()
        user_last_request = cache.get(f'{user_id}')
        if user_last_request:
            user_last_request = user_last_request.strftime(self.format)
        return user_last_request
