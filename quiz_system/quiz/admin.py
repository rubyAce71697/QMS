from django.contrib import admin
from django.http import HttpResponse
from django.conf.urls import url

# Register your models here.
from .models import StudentProfile,QuizInfo,QuizQuestions,StudentQuizAttempts,StudentResponses,TeacherProfile,TeacherS
from django.contrib.auth.models import User
#from .forms import QuizQuestionAdminForm

admin.site.register(StudentProfile)
admin.site.register(StudentQuizAttempts)
admin.site.register(StudentResponses)
#admin.site.register(TeacherProfile)





class QuizInfoAdmin(admin.ModelAdmin):
    list_display = ['quiz_title', 'quizDate']
    ordering = ['quiz_title', 'quizDate']
    
    


class QuizQuestionsAdmin(admin.ModelAdmin):
    #form = QuizQuestionAdminForm

    list_display = ['question','choice_1','choice_2','choice_3','choice_4', 'quiz','isMultipleChoice']
    ordering = ['quiz']
    #fields = ('your_name',)
    #actions = []
    


class TeacherSAdmin(admin.ModelAdmin):
    list_display = ['teacher','student']

class TeacherProfileAdmin(admin.ModelAdmin):
    list_display = ['teacher','doj']



admin.site.register(QuizInfo,QuizInfoAdmin)
admin.site.register(QuizQuestions, QuizQuestionsAdmin)
admin.site.register(TeacherS,TeacherSAdmin)
admin.site.register(TeacherProfile,TeacherProfileAdmin)

#admin.site.register(QuizQuestions)




