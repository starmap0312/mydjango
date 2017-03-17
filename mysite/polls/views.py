# view: type of Web page in your Django application that generally serves a function and has a template
# ex.
#   Question index page  : displays the latest few questions
#   Question detail page : displays a question text, with no results but with a form to vote
#   Question results page: displays results for a particular question
#   Vote action            : handles voting for a particular choice in a particular question
# Each view is responsible for doing one of two things
# 1) return an HttpResponse object containing the content for the requested page, or
# 2) raise an exception, ex. Http404
from django.http import HttpResponse                   # each view either return a HttpResponse or raise an exception
from .models import Question
from django.template import loader                     # used to load a template file
from django.shortcuts import render, get_object_or_404 # shortcut methods for common use cases

# Create your views here.
def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    # 0) write up the template file of polls/templates/polls/index.html 
    # 1) load the template called polls/index.html and passes it a context
    template = loader.get_template('polls/index.html')
    # 2) define a context: a dictionary that maps template variable names to Python objects
    context = {
        'latest_question_list': latest_question_list, # latest_question_list: Python object of <QuerySet>
    }
    # 3) pass the context mapping to the template (so that the template variables have the values)
    return HttpResponse(template.render(context, request))
    # 4) shortcut: render([request], [template name], [context]) method
    #   it returns an an HttpResponse object of the given template rendered with the given context
    #   steps 1) and 3) can be shortened as the following using render() method
    #   i.e. render(request, 'polls/index.html', context)

def detail(request, question_id):
    # configure accordingly in polls/urls.py
    # urlpatterns = [
    #     url(r'^(?P<question_id>[0-9]+)/$', views.detail, name='detail')
    # ]
    # ex: /polls/5/ results in a call of detail(request=<HttpRequest object>, question_id='5')
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")       # a view method may also raise an Http404 exception
    # shortcut: get_object_or_404()
    #   the above try/catch construct can be shortened using get_object_or_404() method
    #   i.e. question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})

def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)

def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)
