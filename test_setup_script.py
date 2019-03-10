import os
import django
import sys

if not sys.version_info >= (3, 7):
    raise Exception("You need Python 3.7, this is 2019")

print(os.getcwd())


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "poll.settings")
django.setup()

from polls import models
from django.contrib.auth.models import User

print(os.getcwd())

if os.name == 'nt':
    os.system("del polls\\migrations")
    os.system("del db.sqlite3")
    system_python = 'python'
else:
    system_python = 'python3'
    os.system("rm -rf polls/migrations")
    os.system("rm -rf db.sqlite3")

os.system(f"{system_python} manage.py makemigrations")
os.system(f"{system_python} manage.py makemigrations polls")
os.system(f"{system_python} manage.py migrate")

User.objects.create_superuser('admin', 'admin@example.com', 'hihihi')
User.objects.create_user('test', 'test@test.com', 'hihihi')
User.objects.create_user('test2', 'test2@test.com', 'hihihi2')

default_user = User.objects.get(pk=1)

p = models.Poll.objects.create(title="My Pizza Poll", owner=default_user)

# First question for poll

question1 = models.TextChoicesQuestion.objects.create(
    question_number=1,
    question_text="Favorite Topping?",
    poll=p,
    can_choose_multiple=False,
    others_can_add=False)

q1c1 = models.TextChoice.objects.create(
    text="Pepperoni", choice_number=1,
    question=question1, added_by=default_user)

q1c2 = models.TextChoice.objects.create(
    text="Pineapple", choice_number=2, question=question1,
    added_by=default_user)

q1c2_nuance = models.TextChoiceNuance.objects.create(
    text="Only Hawaiian", choice=q1c2, added_by=default_user)

question2 = models.RankingQuestion.objects.create(
    question_number=2,
    question_text="How much do you like that topping (1-5)?",
    poll=p,
    low_end=1,
    high_end=5)

question3 = models.TextChoicesQuestion.objects.create(
    question_number=3,
    question_text="Where in the US do you live?",
    poll=p,
    can_choose_multiple=False,
    others_can_add=False)

q3c1 = models.TextChoice.objects.create(
    text="West Coast", choice_number=1,
    question=question3, added_by=default_user)

q3c2 = models.TextChoice.objects.create(
    text="East Coast", choice_number=2, question=question3,
    added_by=default_user)

q3c3 = models.TextChoice.objects.create(
    text="Midwest", choice_number=3, question=question3,
    added_by=default_user)

q3c4 = models.TextChoice.objects.create(
    text="Not in US", choice_number=4,
    question=question3, added_by=default_user)

models.ChoiceVote(choice=q1c2, user=default_user).save()
models.ChoiceNuanceVote(nuance=q1c2_nuance, user=default_user).save()
models.RankVote(rank=3.0, question=question2, user_id=1).save()
models.RankVote(rank=2.0, question=question2, user_id=2).save()
models.RankVote(rank=1.0, question=question2, user_id=3).save()

models.ChoiceVote(choice=q3c1, user=default_user).save()

print(question1.get_most_popular())
print(question2.avg_rank())
print(question3.get_most_popular())

print(p.serialize_to_json())

# import logging
# l = logging.getLogger('django.db.backends')
# l.setLevel(logging.DEBUG)
# l.addHandler(logging.StreamHandler())
# print(question2.avg_rank())
