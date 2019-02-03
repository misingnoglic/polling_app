from django.db import models
from django.contrib.auth.models import User
from django.db.models import Avg


class Poll(models.Model):
    title = models.CharField(max_length=100)
    # Setting null to true in case user deletes their account.
    # We still want to keep the poll.
    owner = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    published = models.BooleanField(default=False)

    def __str__(self):
        return f"#{self.pk} - {self.title}"

    def get_questions(self):
        return Question.objects.filter(poll=self)


class Question(models.Model):
    # Which number question on the poll. (E.g. first, second, third)
    question_number = models.PositiveSmallIntegerField()
    # What the question is.
    question_text = models.CharField(max_length=100)
    # The poll which this question is part of.
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.question_text} - Question #{self.question_number} of poll #{self.poll.pk}"

    class Meta:
        abstract = False
        unique_together = (("question_number", "poll"),
                           ("question_text", "poll"))
        ordering = ['poll', 'question_number']


class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        abstract = False


class TextChoicesQuestion(Question):
    can_choose_multiple = models.BooleanField(default=False)
    others_can_add = models.BooleanField(default=False)

    def get_most_popular(self):
        return max(
            TextChoice.objects.filter(question=self),
            key=lambda x: x.num_votes())


class TextChoice(models.Model):
    text = models.CharField(max_length=100)
    choice_number = models.PositiveSmallIntegerField()
    question = models.ForeignKey(TextChoicesQuestion, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.text}"

    class Meta:
        abstract = False
        unique_together = (("question", "choice_number"), ("question", "text"))

    def num_votes(self):
        return ChoiceVote.objects.filter(choice=self).count()


class ChoiceVote(Vote):
    choice = models.ForeignKey(TextChoice, on_delete=models.CASCADE)

    def __str__(self):
        return f"Vote for {self.choice.text}"


class RankingQuestion(Question):
    low_end = models.IntegerField()
    high_end = models.IntegerField()

    def avg_rank(self):
        return RankVote.objects.filter(question=self).aggregate(Avg('rank'))


class RankVote(Vote):
    rank = models.IntegerField()
    question = models.ForeignKey(RankingQuestion, on_delete=models.CASCADE)
