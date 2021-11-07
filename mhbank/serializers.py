from django.contrib.auth.models import User
from rest_framework import serializers
from mhbank.models import *
from django.db import transaction
from django.utils import timezone
import json
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
        extra_kwargs = {'writer': {'read_only': True}, 'publish_date': {'read_only': True}}



class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = '__all__'
        extra_kwargs = {'account': {'read_only': True}}



class HardnessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hardness
        exclude = ['question']


class QuestionSerializer(serializers.ModelSerializer):
    #answers = AnswerSerializer(many=True)
    hardness = HardnessSerializer()
    comments = CommentSerializer(many=True)
    class Meta:
        model = Question
        fields = '__all__'
        extra_kwargs = {'question_maker': {'read_only': True}, 'publish_date': {'read_only': True}}

    @transaction.atomic
    def create(self, validated_data):
        #answers_data = validated_data.pop('answers')
        comments_data = validated_data.pop('comments')
        hardness_data = validated_data.pop('hardness')
        tags_data = validated_data.pop('tags')
        sub_tags_data = validated_data.pop('sub_tags')
        events_data = validated_data.pop('events')
        validated_data['publish_date'] = timezone.localtime()
        validated_data['score'] = 0

        instance = Question.objects.create(**validated_data)
        hardness = Hardness.objects.create(**hardness_data)
        hardness.question = instance
        hardness.save()
        instance.tags.set(tags_data)
        instance.sub_tags.set(sub_tags_data)
        instance.events.set(events_data)
        instance.save()
        return instance

    @transaction.atomic
    def update(self, instance, validated_data):   
        validated_data.pop('comments')
        validated_data.pop('score')
        Hardness.objects.filter(question=instance).update(**validated_data.pop('hardness'))
        instance.tags.set(validated_data.pop('tags'))
        instance.sub_tags.set(validated_data.pop('sub_tags'))
        instance.events.set(validated_data.pop('events'))
        instance.change_date = timezone.localtime()
        instance.save()
        Question.objects.filter(id=instance.id).update(**validated_data)
        instance = Question.objects.filter(id=instance.id)[0]
        return instance

# class QuestionPropertiesSerializer(serializers.ModelSerializer):
#     # answers = AnswerSerializer(many=True)
#     hardness = HardnessSerializer()

#     class Meta:
#         model = Question
#         fields = ['name', 'verification_status', 'verification_comment', 'tags_name', 'sub_tags_name', \
#             'events_name', 'source_name', 'source_name', 'question_maker_name', 'text', 'publish_date', \
#             'change_date', 'hardness']
        
#         extra_kwargs = {'question_maker': {'read_only': True}, 'publish_date': {'read_only': True}}

# class ShortQuestionSerializer(serializers.ModelSerializer):
#     # answers = AnswerSerializer(many=True)
#     hardness = HardnessSerializer()

#     class Meta:
#         model = Question
#         fields = '__all__'

#         exclude = ['text', 'source', 'events', 'question_maker', 'sub_tags', 'publish_date']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']
        extra_kwargs = {'password': {'write_only': True}}


class PublicAccountSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Account
        exclude = ['phone_number', 'email']


class PrivateAccountSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Account
        fields = '__all__'
        extra_kwargs = {'scientific_rate': {'read_only': True}, 'contribution_rate': {'read_only': True}}

    def create(self, validated_data):
        user = User.objects.create(username=validated_data['user']['username'])
        user.set_password(validated_data['user']['password'])
        user.save()
        validated_data['user'] = user
        return Account.objects.create(**validated_data)


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class SubTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sub_tag
        fields = '__all__'


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'


class SourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Source
        fields = '__all__'


class FilterSerializer(serializers.Serializer):
    sub_tags = serializers.ListField(child=serializers.IntegerField())
    tags = serializers.ListField(child=serializers.IntegerField())
    verification_status = serializers.ListField(child=serializers.CharField())
    events = serializers.ListField(child=serializers.IntegerField())
    sources = serializers.ListField(child=serializers.IntegerField())
    question_makers = serializers.ListField(child=serializers.IntegerField())
    publish_date_from = serializers.DateTimeField()
    publish_date_until = serializers.DateTimeField()
    appropriate_grades_min = serializers.IntegerField(default=-1)
    appropriate_grades_max = serializers.IntegerField(default=-1)
    level_min = serializers.IntegerField(default=-1)
    level_max = serializers.IntegerField(default=-1)
    page = serializers.IntegerField()

class ScoreQuestionSerializer(serializers.Serializer):
    question = serializers.IntegerField(default=-1)
    score = serializers.IntegerField(default=0)


class QuestionPageSerializer(serializers.Serializer):
    # answers = AnswerSerializer(many=True)
    questions = serializers.ListField(child=QuestionSerializer())
    num_pages = serializers.IntegerField()


class LessonPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonPlan
        fields = '__all__'
        extra_kwargs = {'writer': {'read_only': True}, 'publish_date': {'read_only': True}}

    @transaction.atomic
    def create(self, validated_data):
        question_data = validated_data.pop('questions')
        tags_data = validated_data.pop('tags')
        sub_tags_data = validated_data.pop('sub_tags')
        validated_data['publish_date'] = timezone.localtime()
        
        instance = LessonPlan.objects.create(**validated_data)
        instance.questions.set(question_data)
        instance.tags.set(tags_data)
        instance.sub_tags.set(sub_tags_data)
        instance.save()
        return instance

    @transaction.atomic
    def update(self, instance, validated_data):   
        instance.questions.set(validated_data.pop('questions'))
        instance.tags.set(validated_data.pop('tags'))
        instance.sub_tags.set(validated_data.pop('sub_tags'))
        instance.change_date = timezone.localtime()
        instance.save()
        LessonPlan.objects.filter(id=instance.id).update(**validated_data)
        instance = LessonPlan.objects.filter(id=instance.id)[0]
        return instance








# from mhbank.models import Question
# from mhbank.serializers import *
# q = Question.objects.all()[0]
# p = convert_question_to_global_problem_json(q)
# bp = BankProblemSerializer(p)
# from rest_framework.response import Response
# Response(bp, content_type="application/json")



class BankAccountSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.CharField()
    phone_number = serializers.CharField()

class BankSubtopicSerializer(serializers.Serializer):
    topic = serializers.CharField()
    title = serializers.CharField()

class BankBaseProblemSerializer(serializers.Serializer):
    title = serializers.CharField()
    topics = serializers.ListField(child=serializers.CharField())
    subtopics = serializers.ListField(child=BankSubtopicSerializer())
    source = serializers.CharField()
    difficulty = serializers.CharField()
    suitable_for_over = serializers.IntegerField()
    suitable_for_under = serializers.IntegerField()
    is_checked = serializers.BooleanField()

class BankCommentSerializer(serializers.Serializer):
    text = serializers.CharField()
    author = BankAccountSerializer()
    
class BankProblemSerializer(serializers.Serializer):
    base_problem = BankBaseProblemSerializer(many=False)

    problem_type = serializers.CharField()
    title = serializers.CharField()
    
    author = BankAccountSerializer()

    text = serializers.CharField()
    publish_date =  serializers.DateTimeField()
    last_change_date =  serializers.DateTimeField()
    is_private = serializers.BooleanField()
    upvoteCount = serializers.IntegerField()
    
    # comments = serializers.ListField(child=BankCommentSerializer())
    #answer = serializers.TextField()
    
def convert_level_to_difficulty(level):
    maxlevel = 100
    if level/maxlevel < 0.2:
        return 'VeryEasy'
    elif level/maxlevel < 0.4:
        return 'Easy'
    elif level/maxlevel < 0.6:
        return 'Medium'
    elif level/maxlevel < 0.8:
        return 'Hard'
    else:
        return 'VeryHard'

def convert_appropriate_grades_to_grade(grade_min, grade_max):
    maxlevel = 100
    if level/maxlevel < 0.2:
        return 'VeryEasy'
    elif level/maxlevel < 0.4:
        return 'Easy'
    elif level/maxlevel < 0.6:
        return 'Medium'
    elif level/maxlevel < 0.8:
        return 'Hard'
    else:
        return 'VeryHard'


def convert_question_to_global_problem(question):
    class Problem():
        pass
    problem = Problem()
    problem = Problem()
    problem.title = question.name
    problem.topics = [tag.name for tag in question.tags.all()]
    problem.subtopics = []
    for subtag in question.sub_tags.all():
        st = Problem()
        st.topic = subtag.parent.name
        st.title = subtag.name
        problem.subtopics.append(st)
    problem.source = question.source.name if question.source else None
    problem.difficulty = convert_level_to_difficulty(question.hardness.level)
    problem.suitable_for_over = \
        convert_appropriate_grades_to_grade(question.hardness.appropriate_grades_min,\
        question.hardness.appropriate_grades_max)
    problem.is_checked = False
    
    problem.problem_type = 'DescriptiveProblem'
    
    problem.author = Problem()
    problem.author.email = question.question_maker.email
    problem.author.phone_number = question.question_maker.phone_number
    problem.author.first_name = question.question_maker.first_name
    problem.author.last_name = question.question_maker.last_name
    
    problem.text = question.text
    problem.publish_date = question.publish_date
    problem.last_change_date = question.change_date
    problem.is_private = False
    problem.upvote_count = question.score
    problem.copied_from = None
    
    # problem.answer = question.answer.text

    # problem.comments = []
    # for comment in question.comments.all():
    #     c = Problem()
    #     c.text = comment.text
    #     c.author = Problem()
    #     c.author.email = comment.writer.email
    #     problem.comments.append(c)
    return problem
    
def convert_all_question_to_global_problem_json():
    problems = []
    for question in Question.objects.all():
        problem = convert_question_to_global_problem(question)
        problems.append(problem)
    problems_json = json.dumps(BankProblemSerializer(problems, many=True).data, ensure_ascii=False)
    return problems_json