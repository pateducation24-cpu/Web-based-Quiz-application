from django.db import models
from django.contrib.auth.models import User

class Quiz(models.Model):
    """Quiz model - represents a collection of questions"""
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return self.name
    
    def total_questions(self):
        return self.questions.count()
    
    class Meta:
        ordering = ['-created_at']

class Question(models.Model):
    """Question model - individual quiz questions"""
    DIFFICULTY_CHOICES = [
        ('Easy', 'Easy'),
        ('Medium', 'Medium'),
        ('Hard', 'Hard'),
        ('Expert', 'Expert'),
    ]
    
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()
    option1 = models.CharField(max_length=500)
    option2 = models.CharField(max_length=500)
    option3 = models.CharField(max_length=500)
    option4 = models.CharField(max_length=500)
    correct_answer = models.CharField(max_length=500)
    category = models.CharField(max_length=100, default='General')
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, default='Medium')
    points = models.IntegerField(default=10)
    
    def __str__(self):
        return self.text[:50]
    
    def get_options(self):
        """Return options as a list"""
        return [self.option1, self.option2, self.option3, self.option4]
    
    class Meta:
        ordering = ['category', 'difficulty']

class QuizResult(models.Model):
    """Store quiz results for users"""
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score = models.IntegerField()
    total_possible = models.IntegerField()
    percentage = models.FloatField()
    time_taken = models.FloatField(help_text="Time taken in seconds")
    completed_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.quiz.name} - {self.percentage}%"
    
    class Meta:
        ordering = ['-completed_at']

class UserAnswer(models.Model):
    """Store each answer for a quiz attempt"""
    result = models.ForeignKey(QuizResult, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user_answer = models.CharField(max_length=500)
    is_correct = models.BooleanField()
    points_earned = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.question.text[:30]} - {'Correct' if self.is_correct else 'Wrong'}"
