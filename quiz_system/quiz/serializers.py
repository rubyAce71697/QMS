from rest_framework import serializers
from django.contrib.auth.models import User
from .models import TeacherS,TeacherProfile,QuizInfo,QuizQuestions,StudentQuizAttempts,StudentProfile,StudentResponses


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username','first_name','last_name','email')

class StudentProfileSerializer(serializers.ModelSerializer):
    student = UserSerializer(read_only=True)
    class Meta:
        model = StudentProfile
        fields = '__all__'

class TeacherSerializer(serializers.ModelSerializer):

    student = StudentProfileSerializer(read_only=True)
    class Meta:
        model = TeacherS
        fields = ('teacher','student')







class QuizQuestionsSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = QuizQuestions
        fields = ('quiz','question','isMultipleChoice','choice_1','choice_2','choice_3','choice_4','answer')

class StudentResponsesSerializer(serializers.ModelSerializer):
    #student = StudentProfileSerializer(read_only=True)
    question = QuizQuestionsSerializer(read_only=True)
    class Meta:
        model = StudentResponses

        exclude = ['student']


class TeacherProfileSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('teacher','doj')


class QuizInfoSerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = QuizInfo
        fields = ('id','quiz_title','quizDate','quizTime')

class QuizAttemptsSerializer(serializers.ModelSerializer):
    quiz =QuizInfoSerializer(read_only=True)
    class Meta:
        model = StudentQuizAttempts
        fields = ('quiz','attempt_date','score')



