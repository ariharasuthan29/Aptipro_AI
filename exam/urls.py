from django.urls import path
from . import views

urlpatterns = [
    # Auth
    path('', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),

    # Student Module
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('practice/', views.practice_view, name='practice'),
    path('practice/submit/', views.submit_practice_view, name='submit_practice'),
    path('leaderboard/', views.leaderboard_view, name='leaderboard'),

    # Exam Module
    path('exam/start/', views.exam_start_view, name='exam_start'),
    path('exam/launch/', views.start_exam_session_view, name='start_exam_session'),
    path('exam/room/<uuid:session_key>/', views.exam_room_view, name='exam_room'),
    path('exam/finish/<uuid:session_key>/', views.finish_exam_view, name='finish_exam'),
    path('exam/result/<uuid:session_key>/', views.result_view, name='exam_result'),

    # Ajax APIs for Proctoring & Answers
    path('api/exam/submit-response/', views.submit_exam_response_api, name='submit_response_api'),
    path('api/proctor/analyze-frame/', views.analyze_frame_api, name='analyze_frame_api'),
    path('api/proctor/log-violation/', views.log_violation_api, name='log_violation_api'),

    # Admin Control Panel & Excel Importer
    path('admin-dashboard/', views.admin_dashboard_view, name='admin_dashboard'),
    path('admin-dashboard/questions/', views.admin_questions_view, name='admin_questions'),
    path('admin-dashboard/violations/', views.admin_violations_view, name='admin_violations'),
    path('admin-dashboard/export-sample-template/', views.export_sample_excel_template_view, name='export_sample_excel_template'),
    path('admin-dashboard/import-questions/', views.import_excel_questions_view, name='import_excel_questions'),
]
