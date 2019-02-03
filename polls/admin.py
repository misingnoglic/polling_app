from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register([Poll, Question, Vote, TextChoicesQuestion, TextChoice,
                    ChoiceVote, RankingQuestion, RankVote])