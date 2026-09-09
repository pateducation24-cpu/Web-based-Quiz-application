from django.contrib import admin
from .models import Quiz, Question, QuizResult, UserAnswer

class QuestionInline(admin.TabularInline):
    model = Question
    extra = 3

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ['name', 'total_questions', 'created_at']
    inlines = [QuestionInline]
    search_fields = ['name']

    def save_model(self, request, obj, form, change):
        if not obj.created_by_id:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['text', 'quiz', 'category', 'difficulty', 'correct_answer']
    list_filter = ['quiz', 'category', 'difficulty']
    search_fields = ['text']

@admin.register(QuizResult)
class QuizResultAdmin(admin.ModelAdmin):
    list_display = ['user', 'quiz', 'score', 'percentage', 'completed_at']
    list_filter = ['quiz', 'completed_at']

@admin.register(UserAnswer)
class UserAnswerAdmin(admin.ModelAdmin):
    list_display = ['result', 'question', 'is_correct']
