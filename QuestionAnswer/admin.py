from django.contrib import admin

from .models import Answer, Question


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("id", "text", "created_at")
    search_fields = ("text",)
    ordering = ("-created_at",)


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ("id", "question", "user_id", "created_at")
    search_fields = ("user_id", "text")
    list_filter = ("question",)
