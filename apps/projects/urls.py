from django.urls import path

from .views import get_all_projects

app_name = 'projects'

urlpatterns = [
    path('projects/', get_all_projects, name='get_all_projects'),
]
