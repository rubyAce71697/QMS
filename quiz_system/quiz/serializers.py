from rest_framework import serializers
from django.contrib.auth.models import User
from .models import TeacherS,TeacherProfile,QuizInfo,QuizQuestions,StudentQuizAttempts,StudentProfile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username','first_name','last_name','email')


class TeacherSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        fields = ('teacher','student')



class StudentProfileSerializer(serializers.ModelSerializer):
    student = UserSerializer(read_only=True)
    class Meta:
        model = StudentProfile
        fields = '__all__'

class QuizQuestionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizQuestions
        fields = ('quiz','question','isMultipleChoice','choice_1','choice_2','choice_3','choice_4')

class TeacherProfileSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('teacher','doj')


class QuizInfoSerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = QuizInfo
        fields = ('id','quiz_title','quizDate','quizTime')

class QuizAttemptsSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentQuizAttempts
        fields = ('id','quiz','attempt_date','score')

