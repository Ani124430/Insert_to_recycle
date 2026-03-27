from django.urls import path
from . import views

urlpatterns = [
    path('', views.leaderboard_view, name='leaderboard'),
    path('rate/<int:creation_id>/', views.rate_creation_view, name='rate'),
]