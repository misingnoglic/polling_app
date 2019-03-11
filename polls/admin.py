from django.contrib import admin
from .models import *
# Register your models here.


class QuestionInline(admin.TabularInline):
    model = Question


class RankingQuestionInline(admin.TabularInline):
    show_change_link = True
    model = RankingQuestion


class TextChoiceQuestionInline(admin.TabularInline):
    show_change_link = True
    model = TextChoicesQuestion


class TextChoiceInline(admin.TabularInline):
    show_change_link = True
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
class TextChoicesQuestionAdmin(admin.ModelAdmin):
    inlines = [
        TextChoiceInline
    ]


admin.site.register([
    TextChoice, ChoiceVote, RankingQuestion, RankVote, TextChoiceNuance])
