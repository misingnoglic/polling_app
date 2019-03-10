from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponse
from .models import Poll
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
def vote(request, poll_id):
    if request.method == "POST":
        return HttpResponse("Lol you can't actually vote.")
    poll = Poll.objects.prefetch_related(*constants.POLL_PREFETCH_FIELDS).get(
        id=poll_id)
    return render(request, 'vote.html', context={'poll': poll})