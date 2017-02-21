from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
import datetime

# Create your models here.


class StudentProfile(models.Model):
    
    student = models.ForeignKey(User,to_field='username' , on_delete=models.CASCADE,blank=True, null=True,unique = True)
    school = models.CharField(max_length = 200, blank=True, null=True)
    standard = models.PositiveSmallIntegerField(blank=True, null=True)
    doj = models.DateField(default = datetime.date.today, blank=True, null=True)




class QuizInfo(models.Model):
    
    quiz_title = models.CharField(max_length = 100)
    quizDate = models.DateField(default = datetime.date.today)
    quizTime = models.TimeField(default = datetime.time)

    def __unicode__(self):
        return self.quiz_title  


class StudentQuizAttempts(models.Model):
    student = models.ForeignKey(StudentProfile ,to_field='student',blank=True, null=True)
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
        return '{}: {}'.format(self.quiz,self.question)

class StudentResponses(models.Model):
    student = models.ForeignKey(StudentProfile, to_field='student',blank=True, null=True)
    quiz = models.ForeignKey(QuizInfo)
    question = models.ForeignKey(QuizQuestions)
    response = models.CharField(max_length = 200, blank=True, null=True)

    class Meta:
        unique_together = (('student','quiz','question'),)
    
        def __unicode__(self):
            return '{} {} {}'.format(student,quit,question)

class TeacherProfile(models.Model):
    teacher = models.ForeignKey(User,to_field='username')
    doj = models.DateField(default = datetime.date.today, blank=True, null=True)

    class Meta:
        def __unicode__(self):
            return self.teacher


class TeacherS(models.Model):
    teacher = models.ForeignKey(TeacherProfile)
    student = models.ForeignKey(StudentProfile)

    class Meta:
        unique_together = (('teacher','student' ),)
        def __unicode__(self):
            return "{}:{}".format(self.teacher, self.student)

