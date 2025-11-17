from rest_framework import serializers

from .models import Answer, Question


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ["id", "question_id", "user_id", "text", "created_at"]
        read_only_fields = ["id", "question_id", "created_at"]


class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ["id", "text", "created_at", "answers"]
        read_only_fields = ["id", "created_at", "answers"]

