from django.db import models


class Question(models.Model):
    name = models.CharField(max_length=200)
    level = models.IntegerField()
    verification_status = models.CharField(max_length=50)
    appropriate_grades_min = models.IntegerField(default=1, max_length=2)
    appropriate_grades_max = models.IntegerField(default=12, max_length=2)
    tags = models.ManyToManyField(Tag)
    events = models.ManyToManyField(Event)
    source = models.ForeignKey(Source, on_delete=models.CASCADE)
    question_maker = models.ForeignKey(Account, on_delete=models.CASCADE)
    text = models.CharField()
    answer = models.CharField()
    published_date = models.DateTimeField('date published')

    #themed_qs
    #emoj


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE) #meny to one
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    pub_date = models.DateTimeField('date published')
    publications = models.ManyToManyField(Publication) #meny to meny
    models.OneToOneField(
        Place,
        on_delete=models.CASCADE,
        primary_key=True,
    ) # one to one

class Account(models.Model):
    Username = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    phone_number = models.IntegerField()
    #added_questions
    #attempts
    scintific_rate = models.IntegerField()
    contribution_rate = models.IntegerField()
    email = models.CharField(max_length=200)
    role = models.CharField(max_length=1)
    #image_url ... not complete

class Tag(models.Model):
    name = models.CharField(max_length=200)
    #sub_tags

class Sub_tag(models.Model):
    name = models.CharField(max_length=200)
    parent = models.ForeignKey(Tag, on_delete=models.CASCADE)


class Event(models.Model):
    name = models.CharField(max_length=200)
    #questions

class Source(models.Model):
    name = models.CharField(max_length=200)
    #questions

class Attempt(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    time = models.IntegerField(default=0)
    date = models.DateTimeField()
    attempt = models.ForeignKey(Attempt, on_delete=models.CASCADE)


    
class Themed_q(models.Model):
    name = models.CharField(max_length=200)
    text = models.CharField()
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    