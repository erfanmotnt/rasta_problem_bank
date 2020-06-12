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
