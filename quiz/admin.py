from django.contrib import admin
from .models import (
    Subject, Question, QuestionOption, 
    Quiz, QuizQuestion, StudentQuizAttempt, StudentAnswer
)

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'code']

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['question_text', 'subject', 'question_type', 'marks']
    list_filter = ['subject', 'question_type']

@admin.register(QuestionOption)
class QuestionOptionAdmin(admin.ModelAdmin):
    list_display = ['question', 'option_text', 'is_correct']

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ['title', 'subject', 'duration_minutes', 'total_marks', 'is_active']

admin.site.register(QuizQuestion)
admin.site.register(StudentQuizAttempt)
admin.site.register(StudentAnswer)