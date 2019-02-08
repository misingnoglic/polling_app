from django.shortcuts import render
from .models import Poll


# Create your views here.

def index(request):
    fields = [
        'question_set', 'question_set__rankingquestion',
        'question_set__rankingquestion__rankvote_set',
        'question_set__textchoicesquestion',
        'question_set__textchoicesquestion__textchoice_set',
        'question_set__textchoicesquestion__textchoice_set__choicevote_set',
        'question_set__textchoicesquestion__textchoice_set__textchoicenuance_set',
        'question_set__textchoicesquestion__textchoice_set__textchoicenuance_set__choicenuancevote_set',

    ]
    return render(request, 'your_polls.html',
                  context={
                      'polls': Poll.objects.prefetch_related(*fields).all()
                  })
