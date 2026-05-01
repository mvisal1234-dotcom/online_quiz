from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Quiz, StudentQuizAttempt, StudentAnswer

def home(request):
    quizzes = Quiz.objects.filter(is_active=True)
    return render(request, 'home.html', {'quizzes': quizzes})

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        if password != password2:
            messages.error(request, "Passwords do not match!")
        elif User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken!")
        elif User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered!")
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            messages.success(request, "Registration successful! Please login.")
            return redirect('student_login')
    return render(request, 'register.html')

def student_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password!")
    return render(request, 'login.html')

def student_logout(request):
    logout(request)
    return redirect('home')

@login_required
def take_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id, is_active=True)
    
    attempt = StudentQuizAttempt.objects.filter(student=request.user, quiz=quiz).first()
    if attempt and attempt.status == 'completed':
        return redirect('result', attempt_id=attempt.id)

    questions = quiz.quizquestion_set.all()

    if request.method == 'POST':
        attempt = StudentQuizAttempt.objects.create(
            student=request.user,
            quiz=quiz,
            status='completed'
        )

        score = 0
        for q in questions:
            selected_id = request.POST.get(f'question_{q.question.id}')
            if selected_id:
                try:
                    selected_option = q.question.options.get(id=selected_id)
                    is_correct = selected_option.is_correct
                    marks = q.question.marks if is_correct else 0

                    StudentAnswer.objects.create(
                        attempt=attempt,
                        question=q.question,
                        selected_option=selected_option,
                        is_correct=is_correct,
                        marks_obtained=marks
                    )
                    if is_correct:
                        score += marks
                except:
                    pass

        attempt.score = score
        attempt.save()
        return redirect('result', attempt_id=attempt.id)

    return render(request, 'take_quiz.html', {
        'quiz': quiz,
        'questions': questions
    })

@login_required
def result(request, attempt_id):
    attempt = get_object_or_404(StudentQuizAttempt, id=attempt_id, student=request.user)
    return render(request, 'result.html', {'attempt': attempt})