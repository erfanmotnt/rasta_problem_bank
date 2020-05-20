from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

class Account(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE, unique=True, related_name='account')
    first_name = models.CharField(max_length=30, default ='None')
    last_name = models.CharField(max_length=30, default = 'None')
    phone_number = models.CharField(max_length=20)
    email = models.CharField(max_length=200)
    # added_questions
    # attempts
    scientific_rate = models.IntegerField(default=0)
    contribution_rate = models.IntegerField(default=0)
    role = models.CharField(max_length=1)

    # image_url ... not complete

    def __str__(self):
        return self.user.username

    def numberOfAdds(self):
        return len(self.question_set.all())

class Source(models.Model):
    name = models.CharField(max_length=200)
    # questions

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=200)
    # sub_tags
    def __str__(self):
        return self.name

class Sub_tag(models.Model):
    name = models.CharField(max_length=200)
    parent = models.ForeignKey(Tag, on_delete=models.CASCADE)

    def __str__(self):
        return self.name




class Event(models.Model):
    name = models.CharField(max_length=200)
    # questions

    def __str__(self):
        return self.name
        

class Question(models.Model):
    name = models.CharField(max_length=200)
    verification_status = models.CharField(max_length=50)
    tags = models.ManyToManyField(Tag, blank=True)
    sub_tags = models.ManyToManyField(Sub_tag, blank=True)
    events = models.ManyToManyField(Event, blank=True)
    source = models.ForeignKey(Source, blank=True, null=True, on_delete=models.CASCADE)
    question_maker = models.ForeignKey(Account, on_delete=models.CASCADE)
    text = models.CharField(max_length=3000)
    answer = models.CharField(max_length=3000, null=True, blank=True)
    #guidance = models.CharField(max_length=1000)
    publish_date = models.DateTimeField('date published')
    change_date = models.DateTimeField('date changed', default=timezone.localtime())
    # themed_qs
    # emoj

    def __str__(self):
        return self.name

class Hardness(models.Model):
    level = models.IntegerField()
    appropriate_grades_min = models.IntegerField(
        default=1,
        validators=[MaxValueValidator(12), MinValueValidator(1)]
    )
    appropriate_grades_max = models.IntegerField(
        default=12,
        validators=[MaxValueValidator(12), MinValueValidator(1)]
    )
    question = models.OneToOneField(Question, null=True, on_delete=models.CASCADE, related_name='hardness')

    def __str__(self):
        return str(self.level)

class Attempt(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    time = models.IntegerField(default=0)
    date = models.DateTimeField()
    event = models.ForeignKey(Event, on_delete=models.CASCADE)


class Themed_q(models.Model):
    theme = models.CharField(max_length=200)
    text = models.CharField(max_length=3000)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)


'''
from mhbank.models import Question, Hardness
for q in Question.objects.all():
    h = Hardness(level=q.level, appropriate_grades_min=q.appropriate_grades_min, appropriate_grades_max=q.appropriate_grades_max)
    q.hardness=h
    h.save()
'''