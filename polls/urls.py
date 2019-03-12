from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

app_name = "polls"

urlpatterns = [
    path('', views.index, name='index'),
    path('vote/<int:poll_id>', views.vote_on_poll, name='vote'),
    path('yourpolls', views.your_polls, name='your_polls'),
    path('login',
         auth_views.LoginView.as_view(template_name='login.html'),
         name='login'),
    path('logout', auth_views.LogoutView.as_view(), name='logout')
]
