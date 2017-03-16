from django.conf.urls import url

from . import views

# Django supports more elegant URL patterns:
# ex. /newsarchive/<year>/<month>/
#     instead of:
#     /ME2/Sites/dirmod.asp?sid=&type=gen&mod=Core+Pages&gid=A6CD4967199A42D9B65B1B

urlpatterns = [
    url(r'^$', views.index, name='index'),
]
