from django.db import models
from django.contrib.auth.models import User
from django.db.models import Avg, Count
from . import constants
import json


class Poll(models.Model):
    title = models.CharField(max_length=100)
    # Setting null to true in case user deletes their account.
    # We still want to keep the poll.
    owner = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    published = models.BooleanField(default=False)

    def __str__(self):
        return f"#{self.pk} - {self.title}"

    def serialize_to_json(self):
        return json.dumps({
            'id': self.pk,
            'title': self.title,
            'owner': self.owner.pk,
            'published': self.published,
            'questions': [
                # TODO(arya): Prefetch these fields.
                # Use constants.QUESTION_PREFETCH_FIELDS.
                # In the future, make prefetching granular
                # Only prefetch if not called by a method which prefetches).
                q.serialize_to_json() for q in self.question_set.all()]
        })

    class Meta:
        ordering = ['-pk']


class Question(models.Model):
    # Which number question on the poll. (E.g. first, second, third)
    question_number = models.PositiveSmallIntegerField()
    # What the question is.
    question_text = models.CharField(max_length=100)
    # The poll which this question is part of.
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)

    def serialize_to_json(self):
        base = {
            'id': self.pk,
            'question_number': self.question_number,
            'question_text': self.question_text,
            'type': self.get_type()
        }
        base.update(self.get_child_class().serialize_to_json())
        return base

    def __str__(self):
        return f"{self.question_text} - Question #{self.question_number} of poll #{self.poll.pk}"

    def get_type(self):
        for t in constants.QUESTION_TYPES:
            if hasattr(self, t):
                return t
        raise Exception("Invalid Question Type")

    def get_child_class(self):
        t = self.get_type()
        return getattr(self, t)

    class Meta:
        abstract = False
        unique_together = (("question_number", "poll"),
                           ("question_text", "poll"))
        ordering = ['poll', 'question_number']


class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        abstract = True


class TextChoicesQuestion(Question):
    can_choose_multiple = models.BooleanField(default=False)
    others_can_add = models.BooleanField(default=False)

    def get_most_popular(self):
        # TODO(arya): Make this query just with the ORM (use aggregates)
        return max(self.textchoice_set.prefetch_related(
            'choicevote_set').all(), key=lambda x: x.num_votes())

    def serialize_to_json(self):
        return {
            'id': self.pk,
            'can_choose_multiple': self.can_choose_multiple,
            'others_can_add': self.others_can_add,
            'choices': [
                choice.serialize_to_json() for choice in (
                    self.textchoice_set.all())]
        }


class TextChoice(models.Model):
    text = models.CharField(max_length=100)
    choice_number = models.PositiveSmallIntegerField()
    question = models.ForeignKey(TextChoicesQuestion, on_delete=models.CASCADE)
    added_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    def serialize_to_json(self):
        return {
            'id': self.pk,
            'text': self.text,
            'choice_number': self.choice_number,
            'added_by': self.added_by.pk,
            'votes': self.num_votes(),
            'nuances': [
                nuance.serialize_to_json() for nuance in
                self.textchoicenuance_set.all()]
        }

    def __str__(self):
        return f"{self.text}"

    class Meta:
        abstract = False
        unique_together = (("question", "choice_number"), ("question", "text"))
        ordering = ['question__poll', 'question', 'choice_number']

    def num_votes(self):
        return self.choicevote_set.count()


class TextChoiceNuance(models.Model):
    text = models.CharField(max_length=100)
    choice = models.ForeignKey(TextChoice, on_delete=models.CASCADE)
    added_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    def serialize_to_json(self):
        return {
            'id': self.pk,
            'text': self.text,
            'added_by': self.added_by.pk,
            'votes': self.num_votes()
        }

    def num_votes(self):
        return self.choicenuancevote_set.count()


class ChoiceVote(Vote):
    choice = models.ForeignKey(TextChoice, on_delete=models.CASCADE)

    def __str__(self):
        return f"Vote for {self.choice.text}"

    class Meta:
        unique_together = ("choice", "user")


class ChoiceNuanceVote(Vote):
    nuance = models.ForeignKey(TextChoiceNuance, on_delete=models.CASCADE)

    def __str__(self):
        return f"Vote for {self.nuance.text}"

    class Meta:
        unique_together = ("nuance", "user")


class RankingQuestion(Question):
    low_end = models.IntegerField()
    high_end = models.IntegerField()

    def avg_rank(self):
        return self.rankvote_set.all().aggregate(Avg('rank'))['rank__avg']

    def vote_breakdown(self):
        return self.rankvote_set.all().values('rank').annotate(
            total=Count('rank')).order_by('rank')

    def serialize_to_json(self):
        return {
            'id': self.pk,
            'low_end': self.low_end,
            'high_end': self.high_end,
            'votes': list(self.vote_breakdown()),
            'average': self.avg_rank(),
        }


class RankVote(Vote):
    rank = models.IntegerField()
    question = models.ForeignKey(RankingQuestion, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("user", "question")


# One to One relationship with a regular user.
class PollUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birthday = models.DateField(null=True, blank=True)
    # TODO(arya): Figure out how to represent gender & sex & orientation.
    # TODO(arya): Figure out how to do birth country, current location,
    #  states, etc...
    # TODO(arya): Figure out how to do stuff like high school,
    #  highest education completed, college major, job, etc...

