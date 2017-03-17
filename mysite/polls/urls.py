from django.conf.urls import url

from . import views

# Django supports more elegant URL patterns:
# ex. /newsarchive/<year>/<month>/
#     instead of:
#     /ME2/Sites/dirmod.asp?sid=&type=gen&mod=Core+Pages&gid=A6CD4967199A42D9B65B1B

# 1) add an app_name to set the application namespace
#    ex. app_name = 'polls'
# 2) then we can specify the namespaced view in template
#    ex. <li><a href="{% url 'polls:detail' question.id %}">{{ question.question_text }}</a></li>
app_name = 'polls'

urlpatterns = [
    # ex: /polls/
    url(r'^$', views.index, name='index'),
    # ex: /polls/5/
    url(r'^(?P<question_id>[0-9]+)/$', views.detail, name='detail'),
    # ex: /polls/5/results/
    url(r'^(?P<question_id>[0-9]+)/results/$', views.results, name='results'),
    # ex: /polls/5/vote/
    url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),
    # the name arguments help you to remove hardcoded URLs in templates
    #   so that we can change URLs without the need to change the templates accordingly 
    # ex.
    #   <li><a href="/polls/{{ question.id }}/">     {{ question.question_text }}</a></li>
    #   can be written as:
    #   <li><a href="{% url 'detail' question.id %}">{{ question.question_text }}</a></li>
]
