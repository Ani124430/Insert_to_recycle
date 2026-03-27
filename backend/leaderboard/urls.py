from django.urls import path
from . import views

urlpatterns = [
    path('', views.leaderboard, name='leaderboard'),
    path('rate/<int:creation_id>/', views.rate_creation, name='rate'),
]