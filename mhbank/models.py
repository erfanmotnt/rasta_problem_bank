from django.db import models
from django.contrib.auth.models import User

class Account(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE, unique=True, related_name='account')
    phone_number = models.CharField(max_length=20)
    # added_questions
    # attempts
    scientific_rate = models.IntegerField()
    contribution_rate = models.IntegerField()
    email = models.CharField(max_length=200)
    role = models.CharField(max_length=1)
    last_added_question = models.ForeignKey('Question', on_delete=models.CASCADE, null=True, blank=True)

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


class Question(models.Model):
    name = models.CharField(max_length=200)
    level = models.IntegerField()
    verification_status = models.CharField(max_length=50)
    appropriate_grades_min = models.IntegerField(default=1)
    appropriate_grades_max = models.IntegerField(default=12)
    tags = models.ManyToManyField(Tag, blank=True)
    sub_tags = models.ManyToManyField(Sub_tag, blank=True)
    events = models.ManyToManyField(Event, blank=True)
    source = models.ForeignKey(Source, blank=True, null=True, on_delete=models.CASCADE)
    question_maker = models.ForeignKey(Account, on_delete=models.CASCADE)
    text = models.CharField(max_length=3000)
    answer = models.CharField(max_length=3000)
    last_change_date = models.DateTimeField('date published')
    # themed_qs
    # emoj

    def __str__(self):
        return self.name

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

    
