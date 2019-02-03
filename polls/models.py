from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Poll(models.Model):
    title = models.CharField(max_length=100)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL)

class Question(models.Model):
    question_number = models.PositiveSmallIntegerField()
    question_text = models.CharField(max_length=100)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)

class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class TextChoicesQuestion(Question):
    can_choose_multiple = models.BooleanField()
    others_can_add = models.BooleanField()
    pass

class TextChoice(models.Model):
    text = models.CharField(max_length=100)
    choice_number = models.PositiveSmallIntegerField()
    question = TextChoicesQuestion

class ChoiceVote(Vote):
    choice = models.ForeignKey(TextChoice, on_delete=models.CASCADE)

class RankingQuestion(models.Model):
    low_end = models.IntegerField()
    high_end = models.IntegerField()

class RankVote(Vote):
    rank = models.FloatField()
