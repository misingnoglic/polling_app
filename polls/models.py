from django.db import models
from django.contrib.auth.models import User


class Poll(models.Model):
    title = models.CharField(max_length=100)
    # Setting null to true in case user deletes their account.
    # We still want to keep the poll.
    owner = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"#{self.pk} - {self.title}"


class Question(models.Model):
    question_number = models.PositiveSmallIntegerField()
    question_text = models.CharField(max_length=100)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.question_text} - Question #{self.question_number} of poll #{self.poll.pk}"

    class Meta:
        abstract = True


class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        abstract = True


class TextChoicesQuestion(Question):
    can_choose_multiple = models.BooleanField()
    others_can_add = models.BooleanField()


class TextChoice(models.Model):
    text = models.CharField(max_length=100)
    choice_number = models.PositiveSmallIntegerField()
    question = models.ForeignKey(TextChoicesQuestion, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.text}"


class ChoiceVote(Vote):
    choice = models.ForeignKey(TextChoice, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.text}"



class RankingQuestion(models.Model):
    low_end = models.IntegerField()
    high_end = models.IntegerField()
    question = models.ForeignKey(TextChoicesQuestion, on_delete=models.CASCADE)

class RankVote(Vote):
    rank = models.FloatField()
