from uuid import UUID

from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.request import Request

from apps.tasks.models import Tag, Task
from apps.tasks.serializers import TagSerializer, TaskSerializer

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

@api_view(['GET'])
def get_all_tags(request: Request):
    tags = Tag.objects.all()
    serializer = TagSerializer(tags, many=True)
    return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_tag_by_id(request: Request, tag_id: UUID):
    try:
        tag = Tag.objects.get(id=tag_id)
        serializer = TagSerializer(tag)
        return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)
    except Tag.DoesNotExist:
        return JsonResponse({'error': 'Tag not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['PUT'])
def update_tag(request: Request, tag_id: UUID):
    try:
        tag = Tag.objects.get(id=tag_id)
    except Tag.DoesNotExist:
        return JsonResponse({'error': 'Tag not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = TagSerializer(tag, data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return JsonResponse(serializer.data, status=status.HTTP_200_OK)
    return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def create_tag(request: Request):
    serializer = TagSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
    return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)