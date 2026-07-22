from django.contrib import admin
from .models import UserProfile, Category, Question, ExamSession, ExamQuestionResponse, ViolationLog, DailyActivity

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'target_exam', 'daily_streak', 'total_exams', 'average_score', 'highest_score', 'total_points')
    search_fields = ('user__username', 'phone')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'icon')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'category', 'difficulty', 'correct_option', 'created_at')
    list_filter = ('category', 'difficulty')
    search_fields = ('question_text', 'explanation')

@admin.register(ExamSession)
class ExamSessionAdmin(admin.ModelAdmin):
    list_display = ('user', 'mode', 'status', 'score', 'percentage', 'violation_count', 'start_time')
    list_filter = ('mode', 'status')
    search_fields = ('user__username', 'session_key')

@admin.register(ExamQuestionResponse)
class ExamQuestionResponseAdmin(admin.ModelAdmin):
    list_display = ('exam_session', 'question', 'selected_option', 'is_correct')
    list_filter = ('is_correct',)

@admin.register(ViolationLog)
class ViolationLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'violation_type', 'warning_level', 'timestamp', 'exam_session')
    list_filter = ('violation_type', 'warning_level')
    search_fields = ('user__username', 'details')

@admin.register(DailyActivity)
class DailyActivityAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'practice_count', 'score_earned')
