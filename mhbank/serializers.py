from django.contrib.auth.models import User
from rest_framework import serializers
from mhbank.models import *
from django.db import transaction
from django.utils import timezone

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
    tag = serializers.IntegerField(default=-1)
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


class QuestionPageSerializer(serializers.Serializer):
    # answers = AnswerSerializer(many=True)
    questions = serializers.ListField(child=QuestionSerializer())
    num_pages = serializers.IntegerField()
        