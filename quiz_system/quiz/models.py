from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
import datetime

# Create your models here.


class StudentProfile(models.Model):
    
    student = models.OneToOneField(User, on_delete=models.CASCADE)
    school = models.CharField(max_length = 200)
    standard = models.PositiveSmallIntegerField()
    doj = models.DateField(default = datetime.date.today, blank=True, null=True)




class QuizInfo(models.Model):
    
    quiz_title = models.CharField(max_length = 100)
    quizDate = models.DateField(default = datetime.date.today)
    quizTime = models.TimeField(default = datetime.time)

    def __unicode__(self):
        return self.quiz_title  


class StudentQuizAttempts(models.Model):
    student = models.ForeignKey(User)
    quiz = models.ForeignKey(QuizInfo)
    attempt_date = models.DateField(default = datetime.date.today)
    score = models.PositiveSmallIntegerField(default = 0)
    

    class Meta:
        unique_together  = (('student','quiz'),)
    def __unicode__(self):
        return self.quiz.quiz_title

    



   
class QuizQuestions(models.Model):
    quiz = models.ForeignKey(QuizInfo)
    question = models.CharField(max_length = 200)
    isMultipleChoice = models.CharField(max_length = 1)
    choice_1 = models.CharField(max_length = 10, blank=True, null=True)
    choice_2 = models.CharField(max_length = 10, blank=True, null=True)
    choice_3 = models.CharField(max_length = 10, blank=True, null=True)
    choice_4 = models.CharField(max_length = 10, blank=True, null=True)
    answer   = models.CharField(max_length =200, blank=True, null=True)

    def __unicode__(self):
        return self.question

class StudentResponses(models.Model):
    student = models.ForeignKey(User)
    quiz = models.ForeignKey(QuizInfo)
    question = models.ForeignKey(QuizQuestions)
    response = models.CharField(max_length = 200, blank=True, null=True)


