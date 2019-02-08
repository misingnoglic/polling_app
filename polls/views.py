from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Poll

QUESTION_FIELDS = [
    'question_set',
    'question_set__rankingquestion',
    'question_set__rankingquestion__rankvote_set',
    'question_set__textchoicesquestion',
    'question_set__textchoicesquestion__textchoice_set',
    'question_set__textchoicesquestion__textchoice_set__choicevote_set',
    'question_set__textchoicesquestion__textchoice_set__textchoicenuance_set',
    'question_set__textchoicesquestion__textchoice_set__textchoicenuance_set__choicenuancevote_set',
]


def index(request):
    return render(request, 'list_polls.html',
                  context={
                      'polls': Poll.objects.prefetch_related(
                          *QUESTION_FIELDS).all()
                  })


@login_required(login_url='/polls/login')
def your_polls(request):
    return render(request, 'list_polls.html',
                  context={
                      'polls': Poll.objects.prefetch_related(
                          *QUESTION_FIELDS).filter(owner=request.user)
                  })
