from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

class Account(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE, unique=True, related_name='account')
    first_name = models.CharField(max_length=30, default='None')
    last_name = models.CharField(max_length=30, default='None')
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
        self.contribution_rate = len(self.question_set.all())
        self.save()
        return len(self.question_set.all())

    def is_adder(self):
        return self.role == 'a'

    def is_mentor(self):
        return self.role == 'm'

    def is_superuser(self):
        return self.role == 's'


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
    verification_comment = models.CharField(max_length=1000, null=True, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)
    sub_tags = models.ManyToManyField(Sub_tag, blank=True)
    events = models.ManyToManyField(Event, blank=True)
    source = models.ForeignKey(Source, blank=True, null=True, on_delete=models.SET_NULL)
    question_maker = models.ForeignKey(Account, on_delete=models.CASCADE)
    text = models.TextField()
    # answer = models.CharField(max_length=3000, null=True, blank=True)
    # guidance = models.CharField(max_length=1000)
    publish_date = models.DateTimeField('date published')
    change_date = models.DateTimeField(null=True, blank=True)
    #hardness
    # themed_qs
    # emoj

    def __str__(self):
        return self.name


    # def tags_name(self):
    #     query = Tag.objects.filter(question=self.pk)
    #     outList = []
    #     for tag in query:
    #         outList.append(tag.name)
    #     return outList


    # def sub_tags_name(self):
    #     query = Sub_tag.objects.filter(question=self.pk)
    #     outList = []
    #     for tag in query:
    #         outList.append(tag.name)
    #     return outList

    # def events_name(self):
    #     query = Event.objects.filter(question=self.pk)
    #     outList = []
    #     for tag in query:
    #         outList.append(tag.name)
    #     return outList
    
    # def source_name(self):
    #     query = Source.objects.filter(question=self.pk)
    #     return query[0].name if len(query) > 0 else None
    
    # def question_maker_name(self):
    #     query = Account.objects.filter(question=self.pk)
    #     return query[0].user.username
    


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
    text = models.TextField()
    question = models.ForeignKey(Question, on_delete=models.CASCADE)


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=True, related_name='answers')
    text = models.TextField()
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    change_date = models.DateTimeField(null=True, blank=True)
    publish_date = models.DateTimeField('date published', null=True, blank=True)

    # guidances
    # comments
    # is it original?(not student writen)
    # likes
    # teaches

class Guidance(models.Model):
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    text = models.TextField()
    change_date = models.DateTimeField(null=True, blank=True)
    publish_date = models.DateTimeField('date published', null=True, blank=True)


class Teach_box(models.Model):
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    goal = models.CharField(max_length=1000, null=True, blank=True)
    expectations = models.CharField(max_length=1000, null=True, blank=True)
    # notes
    time = models.TimeField(null=True)
    generalـprocess = models.CharField(max_length=3000)
    change_date = models.DateTimeField(null=True, blank=True)
    publish_date = models.DateTimeField('date published', null=True, blank=True)


class Comment(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='comments')
    #teach_box = models.ForeignKey(Teach_box, on_delete=models.CASCADE, null=True)
    text = models.TextField()
    writer = models.ForeignKey(Account, on_delete=models.CASCADE)
    publish_date = models.DateTimeField('date published', null=True, blank=True)

    def __str__(self):
        return self.writer.user.username + " " + self.question.name

    
'''
from mhbank.models import Question, Hardness
for q in Question.objects.all():
    h = Hardness(level=q.level, appropriate_grades_min=q.appropriate_grades_min, appropriate_grades_max=q.appropriate_grades_max)
    q.hardness=h
    h.save()
'''
