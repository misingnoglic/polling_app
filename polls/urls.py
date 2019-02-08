from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('yourpolls', views.your_polls, name='your_polls'),
    path('login', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
]