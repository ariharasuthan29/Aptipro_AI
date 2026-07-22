import uuid
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=15, blank=True, null=True)
    target_exam = models.CharField(max_length=100, default='Placement Examination')
    daily_streak = models.PositiveIntegerField(default=1)
    last_login_date = models.DateField(default=timezone.now)
    total_exams = models.PositiveIntegerField(default=0)
    highest_score = models.FloatField(default=0.0)
    average_score = models.FloatField(default=0.0)
    total_points = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    icon = models.CharField(max_length=50, default='bi-journal-code')

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

class Question(models.Model):
    EASY = 'EASY'
    MEDIUM = 'MEDIUM'
    HARD = 'HARD'

    DIFFICULTY_CHOICES = [
        (EASY, 'Easy'),
        (MEDIUM, 'Medium'),
        (HARD, 'Hard'),
    ]

    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='questions')
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, default=EASY)
    question_text = models.TextField()
    code_snippet = models.TextField(blank=True, null=True)
    option_a = models.CharField(max_length=300)
    option_b = models.CharField(max_length=300)
    option_c = models.CharField(max_length=300)
    option_d = models.CharField(max_length=300)
    correct_option = models.CharField(max_length=1, choices=[('A', 'Option A'), ('B', 'Option B'), ('C', 'Option C'), ('D', 'Option D')])
    explanation = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"[{self.difficulty}] {self.category.name}: {self.question_text[:50]}"

class ExamSession(models.Model):
    FULL_EXAM = 'FULL_EXAM'
    PRACTICE = 'PRACTICE'
    MODE_CHOICES = [
        (FULL_EXAM, 'Full Proctored Exam (40 Questions)'),
        (PRACTICE, 'Daily Aptitude Practice'),
    ]

    IN_PROGRESS = 'IN_PROGRESS'
    COMPLETED = 'COMPLETED'
    AUTO_SUBMITTED = 'AUTO_SUBMITTED'
    STATUS_CHOICES = [
        (IN_PROGRESS, 'In Progress'),
        (COMPLETED, 'Completed'),
        (AUTO_SUBMITTED, 'Auto Submitted (Time/Violation)'),
    ]

    session_key = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='exam_sessions')
    mode = models.CharField(max_length=20, choices=MODE_CHOICES, default=FULL_EXAM)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=IN_PROGRESS)
    
    duration_seconds = models.PositiveIntegerField(default=3600)  # 60 Minutes
    remaining_seconds = models.IntegerField(default=3600)
    
    score = models.FloatField(default=0.0)
    percentage = models.FloatField(default=0.0)
    total_questions = models.PositiveIntegerField(default=40)
    correct_answers_count = models.PositiveIntegerField(default=0)
    incorrect_answers_count = models.PositiveIntegerField(default=0)
    unanswered_count = models.PositiveIntegerField(default=0)
    time_taken_seconds = models.PositiveIntegerField(default=0)
    
    violation_count = models.PositiveIntegerField(default=0)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.mode} ({self.status})"

class ExamQuestionResponse(models.Model):
    exam_session = models.ForeignKey(ExamSession, on_delete=models.CASCADE, related_name='responses')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_option = models.CharField(max_length=1, blank=True, null=True)  # A, B, C, D
    is_correct = models.BooleanField(default=False)
    shuffled_options = models.JSONField(default=dict) # E.g. {"A": "option_c", "B": "option_a", ...}

    def __str__(self):
        return f"Response for {self.exam_session.session_key} - Q{self.question.id}"

class ViolationLog(models.Model):
    FULLSCREEN_EXIT = 'FULLSCREEN_EXIT'
    TAB_SWITCH = 'TAB_SWITCH'
    NO_FACE = 'NO_FACE'
    MULTI_FACE = 'MULTI_FACE'
    MOBILE_DETECTED = 'MOBILE_DETECTED'
    CAMERA_OFF = 'CAMERA_OFF'

    VIOLATION_TYPES = [
        (FULLSCREEN_EXIT, 'Exited Full Screen Mode'),
        (TAB_SWITCH, 'Tab Switch / Window Blur'),
        (NO_FACE, 'Face Not Detected'),
        (MULTI_FACE, 'Multiple Faces Detected'),
        (MOBILE_DETECTED, 'Mobile Phone / Suspicious Activity'),
        (CAMERA_OFF, 'Camera Feed Disabled'),
    ]

    exam_session = models.ForeignKey(ExamSession, on_delete=models.CASCADE, related_name='violations')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    violation_type = models.CharField(max_length=30, choices=VIOLATION_TYPES)
    warning_level = models.PositiveIntegerField(default=1) # 1, 2, 3
    timestamp = models.DateTimeField(auto_now_add=True)
    details = models.TextField(blank=True, null=True)
    snapshot = models.ImageField(upload_to='snapshots/%Y/%m/%d/', blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.violation_type} (Strike {self.warning_level})"

class DailyActivity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='daily_activities')
    date = models.DateField(default=timezone.now)
    login_tracked = models.BooleanField(default=True)
    practice_count = models.PositiveIntegerField(default=0)
    score_earned = models.FloatField(default=0.0)

    class Meta:
        unique_together = ('user', 'date')

    def __str__(self):
        return f"{self.user.username} on {self.date}"
