from rest_framework import status, viewsets
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.decorators import api_view, permission_classes

from mhbank.models import Question
from mhbank.views import permissions
from mhbank.serializers import QuestionSerializer


class QuestionView(viewsets.GenericViewSet, mixins.RetrieveModelMixin, mixins.CreateModelMixin, mixins.ListModelMixin,
                   mixins.UpdateModelMixin):
    permission_classes = [permissions.QuestionPermission]
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

# @api_view(['GET', 'PUT', 'DELETE'])
# def question_detail(request, pk):
#     try:
#         question = Question.objects.get(pk=pk)
#     except Question.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)
#
#     if request.method == 'GET':
#         serializer = QuestionSerializer(question)
#         return Response(serializer.data)
#
#     elif request.method == 'PUT':
#         data = JSONParser().parse(request)
#         serializer = QuestionSerializer(question, data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(status=status.HTTP_400_BAD_REQUEST)
#
#     elif request.method == 'DELETE':
#         question.delete()
#         return Response()
#
#
# class question_list(APIView):
#     def get(self, request):
#         question = Question.objects.all()
#         serializer = QuestionSerializer(question, many=True)
#         return Response(serializer.data)
#
#     def post(self, request):
#         data = JSONParser().parse(request)
#         serializer = QuestionSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

'''
@api_view()
@permission_classes((permissions.QuestionPermission,))
def question_property(request, pk):
    
    return Response(q_serializer.data, status=status.HTTP_200_OK)
'''