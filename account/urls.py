from django.urls import path

from .views import get_user_last_activity


urlpatterns = [
    path('user-activity/', get_user_last_activity),
]
