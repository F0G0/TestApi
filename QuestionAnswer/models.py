from django.db import models


class Question(models.Model):
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"Question(id={self.pk})"


class Answer(models.Model):
    question = models.ForeignKey(
        Question,
        related_name="answers",
        on_delete=models.CASCADE,
    )
    user_id = models.CharField(max_length=255)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self) -> str:
        return f"Answer(id={self.pk}, question_id={self.question_id})"
