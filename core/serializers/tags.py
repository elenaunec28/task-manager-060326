from rest_framework.serializers import ModelSerializer
from core.models import Tag

class TagSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']