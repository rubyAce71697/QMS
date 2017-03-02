from django.shortcuts import render,HttpResponseRedirect,get_list_or_404,reverse,get_object_or_404,HttpResponse

# Create your views here.

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import UserForm,UserLoginForm
from .models import StudentProfile,StudentQuizAttempts,StudentResponses,QuizInfo,QuizQuestions,TeacherS
from .models import TeacherProfile
from django.contrib.auth import login, logout,authenticate
from datetime import datetime
from rest_framework.views import APIView
from rest_framework.fields import CurrentUserDefault
from rest_framework import status,response,generics
from rest_framework.response import Response
from serializers import UserSerializer,QuizInfoSerializer,QuizQuestionsSerializer,QuizAttemptsSerializer,StudentProfileSerializer
from serializers import StudentResponsesSerializer
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateView


def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data = request.POST)
        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            registered = True
        else:
            print user_form.errors
    else:
        user_form = UserForm()
        registered = False
    context = dict()
    context['user_form'] = user_form
    context['registered'] = registered
    template_url = 'quiz/register.html'
    return render(request,template_url,context)

@login_required(login_url="/quiz/")
def home(request):
    print '---------------- idsplating home ---------------------------------'
    #show the test attempted

    #check if user is student
    if not request.user.is_staff:
        
        quiz_attempted = StudentQuizAttempts.objects.filter(student_id = request.user.username)
        print quiz_attempted
        for i in quiz_attempted:
            print i.quiz
        

        quiz_remaining = QuizInfo.objects.all().exclude(id__in=quiz_attempted.values('quiz_id') ).filter(quizDate__lte=datetime.today())
        print quiz_remaining.values()
        quiz_tobestarted = QuizInfo.objects.all().exclude(id__in=quiz_attempted.values('quiz_id') ).filter(quizDate__gt=datetime.today())

        print quiz_tobestarted.values()


        context = dict()
        context['quiz_attempts'] = quiz_attempted
        context['quiz_remaining'] = quiz_remaining
        context['quiz_tobestarted'] = quiz_tobestarted
        
        

    else:
        # the user is teacher
        print "requst usrename :", request.user.username
        teacher_username = TeacherProfile.objects.get(teacher_id=request.user)
        print "filtered usrname :",teacher_username
        print "----------------- prining teacher uername -------------------"

        
        student_ids = TeacherS.objects.all().filter(teacher_id = teacher_username.id)
        print student_ids
        for i in student_ids:
            print i.__dict__
        student_profile_id = StudentProfile.objects.all().filter(id__in=student_ids.values('student_id'))
        print student_profile_id
        for i in student_profile_id:
            print i.__dict__

        print "-------***********************************************-------------------"
        user_id = User.objects.all().filter(username__in=student_profile_id.values('student_id'))
        for i in user_id:
            print i.username
        quiz_attempted = StudentQuizAttempts.objects.select_related().filter(student_id__in=student_profile_id)

        total_quizes = QuizInfo.objects.all()
        print "_________________************************___________________________"
        for i in quiz_attempted:
            print i.__dict__
            print i.__dict__['_quiz_cache'].__dict__
        context = {}
        context['students'] = user_id
        context['quiz_attempted'] = quiz_attempted
        context['total_quizes'] = total_quizes
    context['user'] = request.user
    template_url = 'quiz/home.html'


    return render(request,template_url,context )

class StudentProfileView(generics.ListCreateAPIView):
    serializer_class = StudentProfileSerializer

    def list(self,request):
        queryset = self.get_queryset()
        serializer = StudentProfileSerializer(queryset)
        return Response(serializer.data)

    def get_queryset(self):
        student_profile = StudentProfile.objects.get(student_id=self.request.user)
        print self.request.user
        print student_profile
        return student_profile

class StudentResponsesSerializerView(generics.ListCreateAPIView):
    serializer_class = StudentResponsesSerializer
    queryset = StudentResponses.objects.all()

    def list(self,request):
        queryset = self.get_queryset()
        serializer = StudentResponsesSerializer(queryset, many=True)
        return Response(serializer.data)

class QuizAttempts(generics.ListCreateAPIView):
    serializer_class = QuizAttemptsSerializer

    def list(self,request,student_id):
        queryset = self.get_queryset()
        serializer = QuizAttemptsSerializer(queryset,many=True)
        return Response(serializer.data)
    def get_queryset(self):
        student_profile_id = StudentProfile.objects.all().filter(id__in=self.kwargs['student_id'])
        print student_profile_id
        quiz_attempted = StudentQuizAttempts.objects.all().filter(student_id__in=student_profile_id)

        return quiz_attempted

    

class Quizes(LoginRequiredMixin,generics.ListAPIView):
    queryset = QuizInfo.objects.all()
    serializer_class = QuizInfoSerializer

    def list(self, request):
        queryset = self.get_queryset()
        serializer = QuizInfoSerializer(queryset, many=True)
        return Response(serializer.data)
        


class QuizQuestionsView(LoginRequiredMixin,generics.ListAPIView):
    serializer_class = QuizQuestionsSerializer

    def list(self,request,test_id):
        queryset = self.get_queryset()
        serializer = QuizQuestionsSerializer(queryset,many=True)
        return Response(serializer.data)
    def get_queryset(self):
        return QuizQuestions.objects.all().filter(quiz_id=self.kwargs['test_id'])
        


class Home(LoginRequiredMixin,APIView):
    def get(self,request,pk,format='json'):
        if not request.user.is_staff:
            quiz_attempted = StudentQuizAttempts.objects.filter(student_id = request.user.username)
            print quiz_attempted
            for i in quiz_attempted:
                print i.quiz
            return Response(status.HTTP_200_OK)

        else:
            return Response(status.HTTP_204_NO_CONTENT)
        

class UserAttempts(LoginRequiredMixin,APIView):

    
    login_url = '/quiz/login/'
    def get(self,request,pk,format = 'json'):
        #quiz_attempted = StudentQuizAttempts.objects.select_related().filter(student_id__in=student_profile_id)
        #users = User.objects.all().filter(username=pk)
        users = get_list_or_404(User, username=pk)
        user = UserSerializer(users,many=True)
        print user
        print pk
        #print quiz_attempted
        return  Response(user.data)


@login_required(login_url="/quiz/")
def attempt(request, test_id):
    quiz_questions = get_list_or_404(QuizQuestions, quiz_id=test_id)
    print dir(quiz_questions)
    quiz_id = test_id
    return render(request, 'quiz/attempt.html', {'quiz': quiz_questions, 'quiz_id':test_id})



@login_required(login_url="/quiz/")
def detail(request, test_id):
    print "--------------------------- in detail ------------------------------"
    quiz = get_list_or_404(QuizQuestions,quiz_id=test_id)
    print quiz
    answers = get_list_or_404(StudentResponses,quiz_id=test_id,student=request.user.username)
    print answers
    score = get_object_or_404(StudentQuizAttempts,student=request.user.username,quiz_id=test_id)
    context  = dict()
    context['quiz'] = quiz
    context['answers'] = answers
    context['score'] = score
    print score.score
    return render(request, 'quiz/detail.html',context)




@login_required(login_url="/quiz/")
def submit(request,test_id):
    print request.POST
    print request.POST.keys()[1:]
    print test_id
    quiz_questions = QuizQuestions.objects.all().filter( quiz_id=test_id)
    quizobj = QuizInfo.objects.all().get(id=test_id)
    counter = 0
    for i in request.POST.keys():
        if i != 'csrfmiddlewaretoken':
            foo = StudentResponses()
            foo.quiz = quizobj
            print type(request.user)
            foo.student = StudentProfile.objects.get(student=request.user)
            foo.question = QuizQuestions.objects.all().get(id=i)
            foo.response = request.POST[i]
            if foo.response == foo.question.answer:
                counter += 1
            foo.save() 
    #chcking for unattempted questions   
    print ("Checking for unattempted questions\n\n")
    for i in quiz_questions:
        print "iterating : ", i.id
        print "list is : ", request.POST.keys()
        print [x.encode('UTF8') for x in request.POST.keys()]
        print str(i.id) not in [x.encode('UTF8') for x in request.POST.keys()]
        print str(i.id)  in [x.encode('UTF8') for x in request.POST.keys()]
        if str(i.id) not in [x.encode('UTF8') for x in request.POST.keys()]:
            print "Not attempted : " ,i.id
            foo = StudentResponses()
            foo.quiz = quizobj
            foo.student = StudentProfile.objects.get(student=request.user)
            
            foo.question = i
            foo.save()
    foo = StudentQuizAttempts()
    foo.student = StudentProfile.objects.get(student=request.user)
    foo.quiz = quizobj
    foo.score = counter
    foo.save()
    print foo
    return HttpResponseRedirect(reverse('home'))

"""
def user_login(request):
    if request.method == 'POST':
          username = request.POST['username']
          password = request.POST['password']
          
          user = authenticate(username=username, password=password)
          if user is not None:
              if user.is_active:
                  login(request, user)
                  # Redirect to index page.
                  return HttpResponseRedirect(reverse('home'))
              else:
                  # Return a 'disabled account' error message
                  return HttpResponse("You're account is disabled.")
          else:
              # Return an 'invalid login' error message.
              print  "invalid login details " + username + " " + password
              context = {}
              context['form'] = UserLoginForm()
              return render(request,template_name,context)
    
    elif request.user.is_authenticated():
        return HttpResponseRedirect(reverse('home'))
    else:
        # the login is a  GET request, so just show the user the login form.
        template_name = 'quiz/login.html'
        context = {}
        context['form'] = UserLoginForm()
        return render(request,template_name,context)
"""

class UserLogin(APIView):
    context = dict()
    def get(self,request):
        return Response(status.HTTP_501_NOT_IMPLEMENTED)
    
    
    def post(self,request,format = 'json'):
        print request.data
        if not 'username' in request.data or not 'password' in request.data:
            self.context['status'] = 'failed'
            self.context['error'] = "All fields are mandatory"
            return Response(self.context)
        username = request.data['username']
        password = request.data['password']
        print username
        print password

        user = authenticate(username=username,password=password)
        print user
        if user is not None:
            if user.is_active:
                login(request,user)
                
                self.context['status'] = "success"
                self.context['error'] = None
                return Response(self.context)
                #return reverse('home')
            else:
                self.context['status'] = "failed"
                self.context['error'] = "Session Timed Out. Please login again"
                return Response(self.context)
        else:
            print "in else"
            self.context['status'] = "failed"
            self.context['error'] = "Invaild username or password"
            return Response(self.context)        


class UserLogout(LoginRequiredMixin,APIView):
    def get(self, request):
        
        if request.user.is_active:
            logout(request)

            return Response(status.HTTP_200_OK)
        else:
            
            return Response(status.HTTP_400_BAD_REQUEST)



class LoginTemplateView(TemplateView):
    form_class = UserForm
    template_name = 'quiz/login.html'

class HomeTemplateView(TemplateView):
    def get(self,request):
        return render(request,'quiz/home.html')




"""
{
"username":"rubyace71697",
"password":"n15111993."
}
"""