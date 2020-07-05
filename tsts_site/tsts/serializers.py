from rest_framework import serializers
from .models import Answer, Question, T, T_Result


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ('id', 'answer')


class TResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = T_Result
        fields = ('id', 'answered_id', 'question')

    def update(self, instance, validated_data):
        instance.answered_id = validated_data.get('answered_id', instance.answered_id)
        instance.save()
        return instance


class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ('id', 'question', 'answers')


class TSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)
    t_result = TResultSerializer(source='t_result_set', many=True)

    class Meta:
        model = T
        fields = ('id', 't_date', 'status', 'questions', 't_result')
        read_only_fields = ['id', 't_date', 'status', 'questions']
