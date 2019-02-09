from django.contrib.auth.decorators import login_required
from django.shortcuts import render
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
                          *constants.POLL_PREFETCH_FIELDS).filter(owner=request.user)
                  })
