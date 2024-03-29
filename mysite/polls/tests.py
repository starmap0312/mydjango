import datetime
from django.utils import timezone
from django.test import TestCase
from .models import Question

# Create your tests here.

# note: when running tests, a test database is created and destroyed afterwards 
class QuestionMethodTests(TestCase):

    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() should return False for questions whose
        pub_date is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        # we create a Question instance whose pub_date field is 30 days in the future
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently() should return False for questions whose
        pub_date is older than 1 day.
        """
        time = timezone.now() + datetime.timedelta(days=-30)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently() should return True for questions whose
        pub_date is within the last day.
        """
        time = timezone.now() + datetime.timedelta(hours=-1)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)
