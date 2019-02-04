from django.contrib import admin
from .models import *
# Register your models here.


class QuestionInline(admin.TabularInline):
    model = Question


class RankingQuestionInline(admin.TabularInline):
    model = RankingQuestion


class TextChoiceQuestionInline(admin.TabularInline):
    model = TextChoicesQuestion


class TextChoiceInline(admin.TabularInline):
    model = TextChoice


@admin.register(Poll)
class PollAdmin(admin.ModelAdmin):
    inlines = [
        QuestionInline,
        TextChoiceQuestionInline,
        RankingQuestionInline,
    ]


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    inlines = [
        TextChoiceQuestionInline,
        RankingQuestionInline,
    ]


@admin.register(TextChoicesQuestion)
class QTextChoicesQuestionAdmin(admin.ModelAdmin):
    inlines = [
        TextChoiceInline
    ]


admin.site.register([TextChoice, ChoiceVote, RankingQuestion, RankVote, Vote])
