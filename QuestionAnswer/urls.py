from django.urls import path

from .views import (
    AnswerCreateView,
    AnswerDetailView,
    QuestionDetailView,
    QuestionListCreateView,
)

urlpatterns = [
    path("questions/", QuestionListCreateView.as_view(), name="question-list-create"),
    path("questions/<int:id>/", QuestionDetailView.as_view(), name="question-detail"),
    path(
        "questions/<int:id>/answers/",
        AnswerCreateView.as_view(),
        name="answer-create",
    ),
    path("answers/<int:id>/", AnswerDetailView.as_view(), name="answer-detail"),
]

