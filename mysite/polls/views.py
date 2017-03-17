# view: type of Web page in your Django application that generally serves a function and has a template
# ex.
#   Question index page  : displays the latest few questions
#   Question detail page : displays a question text, with no results but with a form to vote
#   Question results page: displays results for a particular question
#   Vote action            : handles voting for a particular choice in a particular question
# Each view is responsible for doing one of two things
# 1) return an HttpResponse object containing the content for the requested page, or
# 2) raise an exception, ex. Http404
# Generic views:
#   Django provides a shortcut, called the "generic views" system, for common case of basic Web development
#   1) getting data from the database according to a parameter passed in the URL
#   2) loading a template
#   3) returning the rendered template
from django.http import HttpResponse, HttpResponseRedirect # each view either return a HttpResponse or raise an exception
from django.template import loader                         # used to load a template file
from django.shortcuts import render, get_object_or_404     # shortcut methods for common use cases
from django.urls import reverse
from .models import Choice, Question 

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
    # the vote() view redirects to here, showing the results page for the question
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})

# 1) gets the selected_choice object from the database
# 2) computes the new value of votes
# 3) saves it back to the database
# problem: race condition
#   if two users (i.e. two Python threads) of your website try to vote at exactly the same time, this might go wrong
#   ex. two users save the new value of 43, but it should be 44 
# solution:
#   using F()
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        # 1) request.POST:
        #    a dictionary-like object that lets you access submitted data by key name
        #    i.e. request.POST['choice'] returns the ID of the selected choice, as a string
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        #    it will raise KeyError if choice wasn't provided in POST data
        # 2) Redisplay the question voting form.
        return render(
            request,
            'polls/detail.html',
            {
                'question': question,
                'error_message': "You didn't select a choice.",
            }
        )
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # HttpResponseRedirect([url]):
        #   it takes a argument, the URL, to which the user will be redirected 
        # reverse() function:
        #   the function helps avoid having to hardcode a URL in the view function
        #   ex. the following reverse() method returns: '/polls/3/results/', where 3 is value of question.id
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
        # note: always return an HttpResponseRedirect after successfully dealing
        #       with POST data. This prevents data from being posted twice if a
        #       user hits the Back button.
