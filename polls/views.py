from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import render, HttpResponse, redirect, reverse
from .models import Poll, RankVote, ChoiceVote, TextChoice
from . import constants


def index(request):
    return render(request, 'list_polls.html',
                  context={
                      'polls': Poll.objects.prefetch_related(
                          *constants.POLL_PREFETCH_FIELDS).all()
                  })


@login_required(login_url='/polls/login')
def your_polls(request):
    return render(request, 'list_polls.html',
                  context={
                      'polls': Poll.objects.prefetch_related(
                          *constants.POLL_PREFETCH_FIELDS).filter(
                          owner=request.user)
                  })


@login_required(login_url='/polls/login')
def vote_on_poll(request, poll_id):
    poll = Poll.objects.prefetch_related(*constants.POLL_PREFETCH_FIELDS).get(
        id=poll_id)
    user = request.user
    if request.method == "POST":
        print(request.POST)
        with transaction.atomic():
            for question in poll.question_set.all():
                choice_raw = request.POST[
                    f'choiceForQuestion{question.question_number}']
                if question.get_type() == 'rankingquestion':
                    choice = choice_raw
                    vote = RankVote(rank=int(choice),
                                    question=question.rankingquestion,
                                    user=user)
                    vote.save()
                elif question.get_type() == 'textchoicesquestion':
                    # TODO: Can vote on multiple...
                    choice = TextChoice.objects.get(pk=choice_raw)
                    vote = ChoiceVote(choice=choice, user=user)
                    vote.save()
        return redirect(reverse('polls:index'))

    return render(request, 'vote.html', context={'poll': poll})
