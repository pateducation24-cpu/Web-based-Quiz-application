from django.urls import path
from . import views

urlpatterns = [
    # Main pages
    path('', views.home, name='home'),
    path('statistics/', views.statistics, name='statistics'),
    
    # Quiz URLs
    path('quiz/<int:quiz_id>/', views.take_quiz, name='take_quiz'),
    path('quiz/<int:quiz_id>/question/<int:question_index>/', views.quiz_question, name='quiz_question'),
    path('quiz/submit-answer/', views.submit_answer, name='submit_answer'),
    path('quiz/<int:quiz_id>/complete/', views.complete_quiz, name='complete_quiz'),
    
    # Results URLs
    path('result/<int:result_id>/', views.quiz_result, name='quiz_result'),
    path('result/<int:result_id>/review/', views.mistake_review, name='mistake_review'),
    
    # Authentication URLs
    path('login/', views.custom_login, name='login'),
    path('logout/', views.custom_logout, name='logout'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    
    # Clear history URL - ADD THIS LINE
    path('profile/clear-history/', views.clear_history, name='clear_history'),
]
