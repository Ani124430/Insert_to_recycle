"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('register/', include('register.urls')),
    path('leaderboard/', include('leaderboard.urls')),  

    path('profile/', include('saveuserinfo.urls')),
    path('leaderboardes/', views.leaderboardes, name='leaderboardes'), 
    path('profile/', views.profile, name='profile'),
    path('newproject/', views.newproject, name='newproject'),
    path('finishedprojects/', views.finishedprojects, name='finishedprojects'),
    path('unfinprojects/', views.unfinprojects, name='unfinprojects'),
    path('second_pic/', views.second_pic, name='second_pic'),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_URL)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])

   



