from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('quiz/<int:quiz_id>/', views.take_quiz, name='take_quiz'),
    path('result/<int:attempt_id>/', views.result, name='result'),
    
    # New Student Auth URLs
    path('register/', views.register, name='register'),
    path('login/', views.student_login, name='student_login'),
    path('logout/', views.student_logout, name='student_logout'),
]