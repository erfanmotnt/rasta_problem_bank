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
        return Response("invalid data", status=status.HTTP_400_BAD_REQUEST)
    data = serializer.validated_data
    data['account'] = request.user.account
    try:
        qinstance = Question.objects.filter(id=data['question'])[0]
    except:
        return Response("invalid question", status=status.HTTP_400_BAD_REQUEST)
    data['question'] = qinstance

    if abs(data['score']) > 1:
        return Response("wrong score", status=status.HTTP_400_BAD_REQUEST)

    try:
        instance = AccountScoreQuestion.objects.filter(question = data['question'],\
                                                        account = data['account'])[0]
        last_score = instance.score
    except:
        instance = AccountScoreQuestion.objects.create(**data)
        last_score = 0
    new_score = max(min(data['score'] + last_score, 1), -1)
    instance.score = new_score
    instance.save()
    delta_score =  new_score - last_score
    qinstance.score += delta_score
    print(delta_score, qinstance.score, last_score)
    qinstance.save()
    return Response({'score': qinstance.score}, status=status.HTTP_200_OK)
