import datetime
from django.db import models
from django.utils import timezone

# use of models:
# 1) Django will create a database schema (CREATE TABLE statements) for this app
# 2) Django will create a Python database-access API for accessing Question and Choice objects
# requirements:
# 1) include the app in our project
#    i.e. add a reference to its configuration class in the INSTALLED_APPS setting
# 2) write up your models (in models.py)
# 3) run "python manage.py makemigrations" to create migrations for those changes
# 4) run "python manage.py migrate" to apply those changes to the database.

# Create your models here.
class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    # each class field is an instance of models.Field class, representing a table column of some type 
    # ex. question_text & pub_date are the column names

    # define our own behavior for a row object
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    # default: <Question: Question object>, so we can define more useful representation of a row 
    def __str__(self):
        return self.question_text

# Django provides a rich database lookup API
# ex.
# 1) Question.objects.filter(id=1)                             # select a row with its id
#    Question.objects.get(pk=1)                                # select a row with its primary key
# 2) Question.objects.filter(question_text__startswith='What') # select CharField rows with starting content string
# 3) Question.objects.get(pub_date__year=django.utils.timezone.now().year) # select DateTimeField by year
# it raises an exception if no row is selected: ex. DoesNotExist: Question matching query does not exist

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    # ForeignKey: define a relationship, i.e. each Choice is related to a single Question
    #   common database relationships: many-to-one, many-to-many, and one-to-one
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text
