from django.urls import path

from .views import (
    create_tag,
    get_all_tags,
    get_all_tasks,
    get_tag_by_id,
    get_task_by_project_name,
    update_tag,
)

app_name = 'tasks'

urlpatterns = [
    path('tasks/', get_all_tasks, name='get_all_tasks'),
    path('tasks/<str:name>/', get_task_by_project_name, name='get_task_by_project_name'),
    path('tags/', get_all_tags, name='get_all_tags'),
    path('tags/<uuid:tag_id>/', get_tag_by_id, name='get_tag_by_id'),
    path('tags/<uuid:tag_id>/update/', update_tag, name='update_tag'),
    path('tags/create/', create_tag, name='create_tag'),
]
