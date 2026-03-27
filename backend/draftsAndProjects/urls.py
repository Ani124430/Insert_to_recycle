from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_project_view, name='create_project'),
    path('<int:project_id>/', views.project_detail_view, name='project_detail'),
    path('<int:project_id>/finish/', views.finish_project_view, name='finish_project'),
    path('user/<str:username>/', views.user_projects_view, name='user_projects'),
]