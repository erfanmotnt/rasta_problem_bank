from django.contrib.auth.models import User
from rest_framework import serializers
from mhbank.models import Question, Account


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['name', 'verification_status', 'verification_comment', 'text',
                  'source', 'events', 'tags', 'sub_tags', 'question_maker',
                  'change_date', 'publish_date']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']


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

    def create(self, validated_data):
        user = User.objects.create(**validated_data['user'])
        validated_data['user'] = user
        return Account.objects.create(**validated_data)
