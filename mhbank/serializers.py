from django.contrib.auth.models import User
from rest_framework import serializers
from mhbank.models import *


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = '__all__'


class HardnessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hardness
        exclude = ['question']


class QuestionSerializer(serializers.ModelSerializer):
    # answers = AnswerSerializer(many=True)
    hardness = HardnessSerializer()

    class Meta:
        model = Question
        fields = '__all__'
        extra_kwargs = {'question_maker': {'read_only': True}, 'publish_date': {'read_only': True}}


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


class SubTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sub_tag


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event


class SourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Source


class FilterSerializer(serializers.Serializer):
    sub_tags = serializers.ListField(child=serializers.IntegerField())
    tag = serializers.IntegerField
    verification_status = serializers.ListField(child=serializers.CharField())
    events = serializers.ListField(child=serializers.IntegerField())
    sources = serializers.ListField(child=serializers.IntegerField())
    question_makers = serializers.ListField(child=serializers.IntegerField())
    publish_date_from = serializers.DateTimeField
    publish_date_until = serializers.DateTimeField
    appropriate_grades_min = serializers.IntegerField
    appropriate_grades_max = serializers.IntegerField
    level_min = serializers.IntegerField
    level_max = serializers.IntegerField
    page = serializers.IntegerField


