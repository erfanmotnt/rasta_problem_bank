from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, get_list_or_404, reverse

from .models import Question, Tag, Source


def index(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'question.html', {'question': question, 'tags': Tag.objects.all(), 'sources': Source.objects.all()})
