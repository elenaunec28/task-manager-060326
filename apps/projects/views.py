from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.request import Request

from apps.projects.models import Project
from apps.projects.serializers import AllProjectsSerializer


@api_view(['GET'])
def get_all_projects(request: Request):
    projects = Project.objects.all()
    serializer = AllProjectsSerializer(projects, many=True)
    return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)
