from django.core.paginator import Paginator
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from mhbank.models import AccountScoreQuestion, Question
from mhbank.serializers import ScoreQuestionSerializer, QuestionPageSerializer
from mhbank.views.permissions import QuestionPermission



@api_view(['POST'])
def score_question(request):
    serializer = ScoreQuestionSerializer(data=request.data)
    if not serializer.is_valid(raise_exception=True):
        return Response(status=status.HTTP_400_BAD_REQUEST)
    data = serializer.validated_data['question']
    data['account'] = request.user.account
    if abs(data['score']) > 1:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    try:
        instance = AccountScoreQuestion.objects.filter(question = data['question'],\
                                                        account = data['account'])[0]
        last_score = instance.score
    except:
        instance = AccountScoreQuestion.objects.create(**data)
        last_score = 0
        
    instance.save()
    delta_score = max(min(data['score'] + last_score, 1), -1) - last_score
    try:
        instance = Question.filter(id=data['question'])[0]
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    instance.score += delta_score
    instance.save()
    return Response({'score': instance.score}, status=status.HTTP_200_OK)
