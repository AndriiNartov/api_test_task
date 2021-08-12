from django.urls import path

from .views import LikeUnlikeAPIView, PostCreateAPIView

urlpatterns = [
    path('create/', PostCreateAPIView.as_view()),
    path('<int:pk>/like/', LikeUnlikeAPIView.as_view()),
]
