from rest_framework import serializers
from mhbank.models import Question, Account

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['name', 'verification_status', 'verification_comment', 'text',
                'source', 'events', 'tags', 'sub_tags', 'question_maker',
                'change_date', 'publish_date']


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['user','first_name', 'last_name', 'role', 'scientific_rate', 'contribution_rate']