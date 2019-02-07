from django.test import TestCase
from django.contrib.auth.models import User
from django.db import IntegrityError

from .models import Poll, TextChoicesQuestion, RankingQuestion,\
    RankVote, TextChoice, ChoiceVote, TextChoiceNuance, ChoiceNuanceVote


class PollTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create(username='Testuser')
        self.user2 = User.objects.create(username='Testuser2')
        self.user3 = User.objects.create(username='Testuser3')
        self.poll = Poll.objects.create(title="My Pizza Poll", owner=self.user1)
        self.question1 = TextChoicesQuestion.objects.create(
            question_number=1,
            question_text="Favorite Topping?",
            poll=self.poll)
        self.q1c1 = TextChoice.objects.create(text="Pepperoni", choice_number=1,
                                              question=self.question1)
        self.q1c2 = TextChoice.objects.create(text="Pineapple", choice_number=2,
                                              question=self.question1)

        self.q1c2_nuance = TextChoiceNuance.objects.create(text="Only Hawaiian",
                                                           choice=self.q1c2,
                                                           added_by=self.user1)

        self.question2 = TextChoicesQuestion.objects.create(
            question_number=2,
            question_text="Favorite Soda?",
            poll=self.poll)
        self.question3 = RankingQuestion.objects.create(
            question_number=3,
            question_text="How much do you like that topping (1-5)?",
            poll=self.poll,
            low_end=1,
            high_end=5)
        ChoiceVote.objects.create(choice=self.q1c1, user=self.user1)
        ChoiceVote.objects.create(choice=self.q1c1, user=self.user2)
        ChoiceVote.objects.create(choice=self.q1c2, user=self.user3)

    def test_can_query_questions_in_order(self):
        questions = list(self.poll.question_set.all())
        self.assertEqual(questions[0].textchoicesquestion,
                         self.question1)
        self.assertEqual(questions[1].textchoicesquestion,
                         self.question2)
        self.assertEqual(questions[2].rankingquestion,
                         self.question3)

    def test_cant_create_multiple_questions_same_number(self):
        with self.assertRaises(IntegrityError):
            TextChoicesQuestion.objects.create(
                          question_number=1,
                          question_text="Favorite Size?",
                          poll=self.poll)

    def test_cant_create_multiple_choices_same_number(self):
        with self.assertRaises(IntegrityError):
            TextChoice.objects.create(
                          choice_number=1,
                          text="Onions",
                          question=self.question1)

    def test_cant_create_multiple_choices_same_text(self):
        with self.assertRaises(IntegrityError):
            TextChoice.objects.create(
                          choice_number=3,
                          text="Pineapple",
                          question=self.question1)

    def test_rank_averaging(self):
        RankVote.objects.create(
            rank=5, question=self.question3, user=self.user1)
        RankVote.objects.create(
            rank=3, question=self.question3, user=self.user2)
        self.assertEquals(self.question3.avg_rank(), 4.0)

    def test_rank_cant_vote_twice(self):
        RankVote.objects.create(
            rank=5, question=self.question3, user=self.user1)
        with self.assertRaises(IntegrityError):
            RankVote.objects.create(
                rank=4, question=self.question3, user=self.user1)

    def test_text_choice_counting(self):
            self.assertEquals(self.q1c1.num_votes(), 2)
            self.assertEquals(self.q1c2.num_votes(), 1)

    def test_text_choice_winner(self):
            self.assertEquals(self.question1.get_most_popular(), self.q1c1)

    def test_question_get_type(self):
        questions = list(self.poll.question_set.all())
        self.assertEqual(questions[0].get_type(), 'textchoicesquestion')
        self.assertEqual(questions[2].get_type(), 'rankingquestion')

    def test_question_get_child_class(self):
        questions = list(self.poll.question_set.all())
        self.assertEqual(questions[0].get_child_class(), self.question1)
        self.assertEqual(questions[2].get_child_class(), self.question3)

    def test_nuance_count(self):
        nuance_vote = ChoiceNuanceVote.objects.create(
            user=self.user1, nuance=self.q1c2_nuance)
        self.assertEqual(
            self.q1c2.textchoicenuance_set.first().num_votes(), 1)
        self.assertEqual(self.q1c2_nuance.choicenuancevote_set.first(),
                         nuance_vote)
