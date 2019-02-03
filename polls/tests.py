from django.test import TestCase
from django.contrib.auth.models import User

from .models import Poll, Question, TextChoicesQuestion


class PollTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create(username='Testuser')
        self.user2 = User.objects.create(username='Testuser2')
        self.poll = Poll.objects.create(title="My Pizza Poll", owner=self.user1)
        self.question1 = TextChoicesQuestion.objects.create(
            question_number=1,
            question_text="Favorite Topping?",
            poll=self.poll)

    def test_can_query_questions(self):
        self.assertEqual(self.poll.get_questions().first().textchoicesquestion,
                         self.question1)
