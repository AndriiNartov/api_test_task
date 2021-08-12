from django.urls import path

from .views import GetLikesCountByDayAPIView

urlpatterns = [
    path('likes-by-day/', GetLikesCountByDayAPIView.as_view()),
]
