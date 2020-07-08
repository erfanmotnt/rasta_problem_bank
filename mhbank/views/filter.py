from mhbank.models import Question

def getQuestionsByFilter(tag = None, sub_tags=[], \
    verification_status=[], events=[], sources=[], question_makers=[], \
         publish_date_from=None, publish_date_until=None, \
         appropriate_grades_min=None, appropriate_grades_max=None, level_min=None, level_max=None):
    
    questions = Question.objects.all()
    
    if tag is not None:
        questions = questions.filter(tags__id=tag)
    

    if len(sub_tags) != 0:
        questions = questions.filter(sub_tags__in=sub_tags).distinct()
    
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

    if appropriate_grades_max is not None:
        questions = questions.filter(hardnes_appropriate_grades_max__lte=appropriate_grades_max)

    if appropriate_grades_min is not None:
        questions = questions.filter(hardnes_appropriate_grades_min__gte=appropriate_grades_min)

    if level_max is not None:
        questions = questions.filter(hardnes_level__lte=level_max)

    if level_min is not None:
        questions = questions.filter(hardnes_level__gte=level_min)
    
    return questions
    
