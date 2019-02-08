from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('yourpolls', views.your_polls, name='your_polls'),
]