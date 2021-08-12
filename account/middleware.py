from django.core.cache import cache
from django.utils import timezone
from rest_framework_simplejwt.backends import TokenBackend


class UpdateLastActivityMiddleware(object):

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_view(self, request, view_func, view_args, view_kwargs):
        assert hasattr(request, 'user'),\
            'The UpdateLastActivityMiddleware requires authentication middleware to be installed.'
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split()[1]
            valid_data = TokenBackend(algorithm='HS256').decode(token, verify=False)
            user_id = valid_data['user_id']
            if user_id:
                cache.set(user_id, timezone.now(), None)
