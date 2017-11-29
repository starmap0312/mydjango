# Generic views
# it abstracts the concepts of:
# 1) ListView  : it abstracts the concepts of display a list of objects
# 2) DetailView: it abstracts the concepts of display a detail page for a particular type of object
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from polls.models import Choice, Question

# Create your views here.
class IndexView(generic.ListView):
    template_name = 'polls_generic/index.html'
    context_object_name = 'latest_question_list'
    # provide the context_object_name attribute, specifying latest_question_list
    #   otherwise, the default is a automatically generated context variable: question_list

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
    model = Question                            # each generic view needs to know what model it will be acting upon
    template_name = 'polls_generic/detail.html' # specify the template name
    # note:
    #   it expects the primary key value captured from the URL to be called "pk"
    #   so we've changed question_id to pk for the generic views
    # the question variable is provided automatically, since we are using a Django model (Question)

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls_generic/results.html'

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(
            request,
            'polls_generic/detail.html',
            {
                'question': question,
                'error_message': "You didn't select a choice.",
            }
        )
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls_generic:results', args=(question.id,)))
