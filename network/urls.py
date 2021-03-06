from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('api/post/', include('post.urls')),
    path('api/analytics/', include('analytics.urls')),
    path('api/account/', include('account.urls')),
]
