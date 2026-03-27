from django.urls import path
from . import views

urlpatterns = [
    path('<str:username>/', views.get_profile, name='get_profile'),
    path('<str:username>/update/', views.update_profile, name='update_profile'),
]
