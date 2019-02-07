from django.shortcuts import render
from .models import Poll


# Create your views here.

def index(request):
    return render(request, 'your_polls.html',
                  context={'polls': Poll.objects.all()})
