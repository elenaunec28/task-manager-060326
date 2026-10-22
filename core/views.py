from django.http import HttpResponse
from .serializers import AllProjectsSerializer, TaskSerializer
from rest_framework.request import Request
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from core.models import Project, Task


def hello(request, name):
    return HttpResponse(f'Hello, {name}!')

@api_view(['GET'])
def get_all_projects(request: Request):
    projects = Project.objects.all()
    serializer = AllProjectsSerializer(projects, many=True)
    return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_all_tasks(request: Request):
    tasks = Task.objects.all()
    serializer = TaskSerializer(tasks, many=True)
    return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_task_by_project_name(request: Request, name: str):
    try:
        task = Task.objects.filter(project__title=name)
        serializer = TaskSerializer(task, many=True)
        return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)
    except Task.DoesNotExist:
        return JsonResponse({'error': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)