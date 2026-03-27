from django.urls import path
from . import views

urlpatterns = [
    path('rate/<int:project_id>/', views.getRating, name='ai_rate'),
]
