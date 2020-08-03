from django.core.paginator import Paginator
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from mhbank.models import Question
from mhbank.serializers import FilterSerializer, QuestionPageSerializer
from mhbank.views.permissions import QuestionPermission


def getQuestionsByFilter(orderField=None ,tag=-1, sub_tags=[], \
                         verification_status=[], events=[], sources=[], question_makers=[], \
                         publish_date_from=None, publish_date_until=None, \
                         appropriate_grades_min=-1, appropriate_grades_max=-1, level_min=-1, level_max=-1, page=None):
    questions = Question.objects.all()
    if tag != -1:
        questions = questions.filter(tags__id=tag)

    if len(sub_tags) != 0:
        questions = questions.filter(sub_tags__in=sub_tags).distinct()

    if len(events) != 0:
        questions = questions.filter(events__in=events).distinct()

    if len(verification_status) != 0:
        questions = questions.filter(verification_status__in=verification_status)

    if len(sources) != 0:
        questions = questions.filter(source__in=sources)

    if len(question_makers) != 0:
        questions = questions.filter(question_maker__in=question_makers)

    if publish_date_until is not None:
        questions = questions.filter(publish_date__lte=publish_date_until)

    if publish_date_from is not None:
        questions = questions.filter(publish_date__gte=publish_date_from)

    if appropriate_grades_max != -1:
        questions = questions.filter(hardness__appropriate_grades_max__lte=appropriate_grades_max)

    if appropriate_grades_min != -1:
        questions = questions.filter(hardness__appropriate_grades_min__gte=appropriate_grades_min)

    if level_max != -1:
        questions = questions.filter(hardness__level__lte=level_max)

    if level_min != -1:
        questions = questions.filter(hardness__level__gte=level_min)

    if orderField is not None:
        questions = questions.order_by(orderField)
    return questions.order_by('id')


def getQuestionsByRemovePermitions(request, questions):
    out_list = []
    qp = QuestionPermission()
    request.method = 'GET'
    for q in questions:
        request.parser_context['kwargs']['pk'] = q.pk
        if qp.has_permission(request, None):
            out_list.append(q)
    return out_list

@api_view(['POST'])
def question_filter(request):
    serializer = FilterSerializer(data=request.data)
    if not serializer.is_valid(raise_exception=True):
        return Response(status=status.HTTP_400_BAD_REQUEST)
    data = serializer.validated_data
    q_list = getQuestionsByRemovePermitions(request, getQuestionsByFilter(**data))
    from django.conf import settings
    paginator = Paginator(q_list, settings.CONSTANTS['PAGINATION_NUMBER'])
    page = paginator.get_page(data.get('page'))
    q_serializer = QuestionPageSerializer({'questions':page.object_list, 'num_pages':paginator.num_pages})
    return Response(q_serializer.data, status=status.HTTP_200_OK)
