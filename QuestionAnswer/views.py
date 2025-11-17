import logging

from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Answer, Question
from .serializers import AnswerSerializer, QuestionSerializer

logger = logging.getLogger(__name__)


class QuestionListCreateView(generics.ListCreateAPIView):
    queryset = Question.objects.prefetch_related("answers").all()
    serializer_class = QuestionSerializer

    def perform_create(self, serializer):
        question = serializer.save()
        logger.info("Question %s created", question.pk)


class QuestionDetailView(generics.RetrieveDestroyAPIView):
    queryset = Question.objects.prefetch_related("answers").all()
    serializer_class = QuestionSerializer
    lookup_url_kwarg = "id"

    def perform_destroy(self, instance):
        question_id = instance.pk
        super().perform_destroy(instance)
        logger.info("Question %s deleted with cascaded answers", question_id)


class AnswerCreateView(APIView):
    def post(self, request, id: int):
        question = get_object_or_404(Question, pk=id)
        serializer = AnswerSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        answer = serializer.save(question=question)
        logger.info(
            "Answer %s created for question %s by user %s",
            answer.pk,
            question.pk,
            answer.user_id,
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class AnswerDetailView(generics.RetrieveDestroyAPIView):
    queryset = Answer.objects.select_related("question").all()
    serializer_class = AnswerSerializer
    lookup_url_kwarg = "id"

    def perform_destroy(self, instance):
        answer_id = instance.pk
        super().perform_destroy(instance)
        logger.info("Answer %s deleted", answer_id)
