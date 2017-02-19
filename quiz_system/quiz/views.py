from django.shortcuts import render,HttpResponseRedirect,get_list_or_404,reverse,get_object_or_404

# Create your views here.

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import UserForm,UserLoginForm
from .models import StudentProfile,StudentQuizAttempts,StudentResponses,QuizInfo,QuizQuestions
from django.contrib.auth import login, logout,authenticate
from datetime import datetime


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
    #show the test attempted
    quiz_attempted = StudentQuizAttempts.objects.filter(student_id = request.user.id)
    print quiz_attempted
    for i in quiz_attempted:
        print i.quiz

    quiz_remaining = QuizInfo.objects.all().exclude(id__in=quiz_attempted.values('quiz_id') ).filter(quizDate__lte=datetime.today())
    print quiz_remaining.values()
    quiz_tobestarted = QuizInfo.objects.all().exclude(id__in=quiz_attempted.values('quiz_id') ).filter(quizDate__gt=datetime.today())
    print quiz_tobestarted.values()


    context = {}
    context['user'] = request.user
    context['quiz_attempts'] = quiz_attempted
    context['quiz_remaining'] = quiz_remaining
    context['quiz_tobestarted'] = quiz_tobestarted
    template_url = 'quiz/home.html'
    return render(request,template_url,context )


@login_required(login_url="/quiz/")
def attempt(request, test_id):
    quiz_questions = get_list_or_404(QuizQuestions, quiz_id=test_id)
    print quiz_questions
    quiz_id = test_id
    return render(request, 'quiz/attempt.html', {'quiz': quiz_questions, 'quiz_id':test_id})



@login_required(login_url="/quiz/")
def detail(request, test_id):
    quiz = get_list_or_404(QuizQuestions,quiz_id=test_id)
    print quiz
    answers = get_list_or_404(StudentResponses,quiz_id=test_id,student=request.user)
    print answers
    score = get_object_or_404(StudentQuizAttempts,student=request.user,quiz_id=test_id)
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
            foo.student = request.user
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
            foo.student = request.user
            
            foo.question = i
            foo.save()
    foo = StudentQuizAttempts()
    foo.student = request.user
    foo.quiz = quizobj
    foo.score = counter
    foo.save()
    print foo
    return HttpResponseRedirect(reverse('home'))


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