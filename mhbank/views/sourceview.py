from rest_framework import status, viewsets
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework import mixins

from mhbank.models import Question
from mhbank.models import Source
from mhbank.views import permissions
from mhbank.serializers import SourceSerializer


class SourceView(viewsets.GenericViewSet, mixins.RetrieveModelMixin, mixins.CreateModelMixin, mixins.ListModelMixin,
                 mixins.UpdateModelMixin):
    permission_classes = [permissions.SourcePermission]
    queryset = Source.objects.all()
    serializer_class = SourceSerializer
