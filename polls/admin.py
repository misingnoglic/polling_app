from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register([Poll, TextChoicesQuestion, TextChoice,
                    ChoiceVote, RankingQuestion, RankVote])
