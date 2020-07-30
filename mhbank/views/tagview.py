from rest_framework import status, viewsets
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework import mixins

from mhbank.models import Question
from mhbank.models import Tag
from mhbank.views import permissions
from mhbank.serializers import TagSerializer


class TagView(viewsets.GenericViewSet, mixins.RetrieveModelMixin, mixins.CreateModelMixin, mixins.ListModelMixin,
              mixins.UpdateModelMixin):
    permission_classes = [permissions.TagPermission]
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
