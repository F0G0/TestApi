from rest_framework import status
from rest_framework.test import APITestCase

from .models import Answer, Question


class QuestionAnswerAPITestCase(APITestCase):
    def setUp(self):
        self.question = Question.objects.create(text="What is Django?")

    def test_create_and_list_questions(self):
        payload = {"text": "Second question"}
        response = self.client.post("/api/questions/", payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Question.objects.count(), 2)

        list_response = self.client.get("/api/questions/")
        self.assertEqual(list_response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(list_response.data), 2)

    def test_get_question_with_answers(self):
        Answer.objects.create(
            question=self.question,
            user_id="user-1",
            text="It is a Python web framework.",
        )
        response = self.client.get(f"/api/questions/{self.question.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["answers"]), 1)

    def test_prevent_answer_creation_for_missing_question(self):
        response = self.client.post(
            "/api/questions/999/answers/",
            {"user_id": "user-1", "text": "Test"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_question_cascades_answers(self):
        Answer.objects.create(
            question=self.question,
            user_id="user-1",
            text="Answer to delete",
        )
        delete_response = self.client.delete(f"/api/questions/{self.question.id}/")
        self.assertEqual(delete_response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Answer.objects.count(), 0)
