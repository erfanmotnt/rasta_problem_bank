from rest_framework import status, viewsets
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.decorators import api_view, permission_classes

from mhbank.models import Comment
from mhbank.views import permissions
from mhbank.serializers import CommentSerializer
from django.db import transaction
from django.utils import timezone


class CommentView(viewsets.GenericViewSet, mixins.RetrieveModelMixin, mixins.CreateModelMixin, mixins.ListModelMixin,
                   mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    permission_classes = [permissions.CommentPermission]
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        data = request.data
        serializer = CommentSerializer(data=data)
        if not serializer.is_valid(raise_exception=True):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        data = serializer.validated_data
        data['writer'] = request.user.account
        data['publish_date'] = timezone.localtime()

        instance = serializer.create(data)
        instance.save()

        response = serializer.to_representation(instance)
        return Response(response)


