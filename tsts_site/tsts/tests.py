from django.test import TestCase
from .models import Question, random_list

class QuestionModelTests(TestCase):

    def test_random_list(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is in the future.
        """
        question_list = random_list(Question, 3)

        self.assertIs(bool(question_list), True)

