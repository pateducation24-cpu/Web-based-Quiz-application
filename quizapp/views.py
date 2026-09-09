from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from django.db.models import Avg
from .models import Quiz, Question, QuizResult, UserAnswer

# Home page
def home(request):
    """Home page showing all quizzes"""
    quizzes = Quiz.objects.all()
    total_quizzes = quizzes.count()
    total_questions = Question.objects.count()
    
    context = {
        'quizzes': quizzes,
        'total_quizzes': total_quizzes,
        'total_questions': total_questions,
    }
    return render(request, 'quizapp/home.html', context)

def quiz_list(request):
    """List all available quizzes"""
    quizzes = Quiz.objects.all()
    return render(request, 'quizapp/home.html', {'quizzes': quizzes})

@login_required
def take_quiz(request, quiz_id):
    """Start a quiz - initialize session"""
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = list(quiz.questions.all())
    
    if not questions:
        messages.error(request, "This quiz has no questions yet!")
        return redirect('quiz_list')
    
    # Store quiz data in session
    request.session['quiz_id'] = quiz.id
    request.session['quiz_name'] = quiz.name
    request.session['total_questions'] = len(questions)
    request.session['score'] = 0
    request.session['current_index'] = 0
    request.session['answers'] = []
    
    # Store questions in session
    questions_data = []
    for q in questions:
        questions_data.append({
            'id': q.id,
            'text': q.text,
            'options': [q.option1, q.option2, q.option3, q.option4],
            'correct_answer': q.correct_answer,
            'category': q.category,
            'difficulty': q.difficulty,
            'points': q.points
        })
    request.session['questions_data'] = questions_data
    request.session.save()
    
    return redirect('quiz_question', quiz_id=quiz.id, question_index=0)

@login_required
def quiz_question(request, quiz_id, question_index):
    """Display a single quiz question"""
    if request.session.get('quiz_id') != quiz_id:
        return redirect('take_quiz', quiz_id=quiz_id)

    questions_data = request.session.get('questions_data', [])

    if question_index < 0 or question_index >= len(questions_data):
        return redirect('complete_quiz', quiz_id=quiz_id)
    
    question = questions_data[question_index]
    progress = int((question_index + 1) / len(questions_data) * 100)
    
    context = {
        'quiz_id': quiz_id,
        'question': question,
        'question_num': question_index + 1,
        'total_questions': len(questions_data),
        'progress': progress,
        'quiz_name': request.session.get('quiz_name'),
        'score': request.session.get('score', 0),
    }
    return render(request, 'quizapp/quiz_question.html', context)

@login_required
def submit_answer(request):
    """Submit answer via AJAX"""
    if request.method == 'POST':
        try:
            quiz_id = int(request.POST.get('quiz_id'))
        except (TypeError, ValueError):
            return JsonResponse({'success': False, 'error': 'Invalid quiz ID.'}, status=400)
        try:
            question_index = int(request.POST.get('question_index', 0))
        except (TypeError, ValueError):
            return JsonResponse({'success': False, 'error': 'Invalid question index.'}, status=400)
        user_answer = request.POST.get('answer', '')
        
        questions_data = request.session.get('questions_data', [])

        if (request.session.get('quiz_id') == int(quiz_id)
                and question_index == request.session.get('current_index', 0)
                and 0 <= question_index < len(questions_data)):
            question = questions_data[question_index]
            is_correct = (user_answer.strip().lower() == question['correct_answer'].strip().lower())
            points_earned = question['points'] if is_correct else 0
            
            # Update score
            current_score = request.session.get('score', 0)
            new_score = current_score + points_earned
            request.session['score'] = new_score
            
            # Store answer
            answers = request.session.get('answers', [])
            answers.append({
                'question_id': question['id'],
                'question_text': question['text'],
                'user_answer': user_answer,
                'correct_answer': question['correct_answer'],
                'is_correct': is_correct,
                'points_earned': points_earned,
                'category': question['category']
            })
            request.session['answers'] = answers
            request.session['current_index'] = question_index + 1
            request.session.save()
            
            return JsonResponse({
                'success': True,
                'is_correct': is_correct,
                'correct_answer': question['correct_answer'],
                'points_earned': points_earned,
                'score': new_score,
                'next_index': question_index + 1,
                'total': len(questions_data)
            })
    
    return JsonResponse({'success': False}, status=400)

@login_required
def complete_quiz(request, quiz_id):
    """Complete the quiz and save results"""
    quiz = get_object_or_404(Quiz, id=quiz_id)
    answers = request.session.get('answers', [])
    score = request.session.get('score', 0)
    
    # Calculate total possible
    questions_data = request.session.get('questions_data', [])
    if (request.session.get('quiz_id') != quiz.id
            or not questions_data
            or request.session.get('current_index', 0) < len(questions_data)):
        messages.error(request, 'Complete the active quiz before viewing its results.')
        return redirect('take_quiz', quiz_id=quiz.id)

    total_possible = sum(q.get('points', 10) for q in questions_data)
    percentage = (score / total_possible * 100) if total_possible > 0 else 0
    
    # Save results to database
    result = QuizResult.objects.create(
        user=request.user if request.user.is_authenticated else None,
        quiz=quiz,
        score=score,
        total_possible=total_possible,
        percentage=percentage,
        time_taken=0
    )
    
    # Save each answer
    for answer in answers:
        question = Question.objects.get(id=answer['question_id'])
        UserAnswer.objects.create(
            result=result,
            question=question,
            user_answer=answer['user_answer'],
            is_correct=answer['is_correct'],
            points_earned=answer['points_earned']
        )
    
    # Clear session
    request.session.pop('quiz_id', None)
    request.session.pop('quiz_name', None)
    request.session.pop('questions_data', None)
    request.session.pop('answers', None)
    request.session.pop('score', None)
    
    return redirect('quiz_result', result_id=result.id)

@login_required
def quiz_result(request, result_id):
    """Display quiz results"""
    result = get_object_or_404(QuizResult, id=result_id, user=request.user)
    
    # Calculate grade
    if result.percentage >= 90:
        grade = "A+"
    elif result.percentage >= 80:
        grade = "A"
    elif result.percentage >= 70:
        grade = "B"
    elif result.percentage >= 60:
        grade = "C"
    else:
        grade = "F"
    
    # Category breakdown
    categories = {}
    for answer in result.answers.all():
        cat = answer.question.category
        if cat not in categories:
            categories[cat] = {'correct': 0, 'total': 0, 'points': 0}
        categories[cat]['total'] += 1
        if answer.is_correct:
            categories[cat]['correct'] += 1
            categories[cat]['points'] += answer.points_earned
    
    context = {
        'result': result,
        'grade': grade,
        'categories': categories,
    }
    return render(request, 'quizapp/quiz_result.html', context)

@login_required
def mistake_review(request, result_id):
    """Review mistakes from a quiz"""
    result = get_object_or_404(QuizResult, id=result_id, user=request.user)
    mistakes = [a for a in result.answers.all() if not a.is_correct]
    
    context = {
        'result': result,
        'mistakes': mistakes,
    }
    return render(request, 'quizapp/mistake_review.html', context)

def statistics(request):
    """Overall statistics"""
    total_quizzes = Quiz.objects.count()
    total_questions = Question.objects.count()
    average = QuizResult.objects.aggregate(average=Avg('percentage'))['average']
    avg_score = average or 0
    
    context = {
        'total_quizzes': total_quizzes,
        'total_questions': total_questions,
        'total_attempts': total_attempts,
        'avg_score': avg_score,
    }
    return render(request, 'quizapp/statistics.html', context)

# Authentication Views
def custom_login(request):
    """Custom login view"""
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'quizapp/login.html', {'form': form})

def custom_logout(request):
    """Custom logout view"""
    if request.method == 'POST':
        logout(request)
    return redirect('home')

def register(request):
    """User registration view"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful! Welcome to QuizApp!')
            return redirect('home')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserCreationForm()
    return render(request, 'quizapp/register.html', {'form': form})

@login_required
def profile(request):
    """User profile view"""
    user_results = QuizResult.objects.filter(user=request.user)
    avg_score = user_results.aggregate(Avg('percentage'))['percentage__avg'] or 0
    
    context = {
        'user': request.user,
        'results': user_results,
        'total_quizzes_taken': user_results.count(),
        'average_score': avg_score,
    }
    return render(request, 'quizapp/profile.html', context)

@login_required
def clear_history(request):
    """Clear user's quiz history"""
    if request.method == 'POST':
        # Delete all quiz results for this user
        results = QuizResult.objects.filter(user=request.user)
        deleted_count = results.count()
        results.delete()
        messages.success(request, f'✅ Successfully cleared {deleted_count} quiz records from your history!')
    return redirect('profile')
