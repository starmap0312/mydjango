from django.db import models

# use of models:
# 1) Django will create a database schema (CREATE TABLE statements) for this app
# 2) Django will create a Python database-access API for accessing Question and Choice objects
# requirements:
# 1) we need to include the app in our project
#    i.e. add a reference to its configuration class in the INSTALLED_APPS setting
# 2) we need to run migrate to create those model tables in database
#    i.e. python manage.py migrate 

# Create your models here.
class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    # each class field is an instance of models.Field class, representing a table column of some type 
    # ex. question_text & pub_date are the column names


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    # ForeignKey: define a relationship, i.e. each Choice is related to a single Question
    #   common database relationships: many-to-one, many-to-many, and one-to-one
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
