import os
import django

print(os.getcwd())


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "poll.settings")
django.setup()

from polls import models
from django.contrib.auth.models import User

print(os.getcwd())

os.system("del polls\\migrations")
os.system("del db.sqlite3")
os.system("python manage.py makemigrations")
os.system("python manage.py makemigrations polls")
os.system("python manage.py migrate")

User.objects.create_superuser('admin', 'admin@example.com', 'hihihi')

default_user = User.objects.get(pk=1)

p = models.Poll(title="My Pizza Poll", owner=default_user)
p.save()

# First question for poll

question1 = models.TextChoicesQuestion(
    question_number=1,
    question_text="Favorite Topping?",
    poll=p,
    can_choose_multiple=False,
    others_can_add=False)
question1.save()

q1c1 = models.TextChoice(text="Pepperoni", choice_number=1, question=question1)
q1c1.save()
q1c2 = models.TextChoice(text="Pineapple", choice_number=2, question=question1)
q1c2.save()


question2 = models.RankingQuestion(
    question_number=2,
    question_text="How much do you like that topping (1-5)?",
    poll=p,
    low_end=1,
    high_end=5)

question2.save()

question3 = models.TextChoicesQuestion(
    question_number=3,
    question_text="Where in the US do you live?",
    poll=p,
    can_choose_multiple=False,
    others_can_add=False)
question3.save()

q3c1 = models.TextChoice(text="West Coast", choice_number=1, question=question3)
q3c1.save()
q3c2 = models.TextChoice(text="East Coast", choice_number=2, question=question3)
q3c2.save()
q3c3 = models.TextChoice(text="Midwest", choice_number=3, question=question3)
q3c3.save()
q3c4 = models.TextChoice(text="Not in US", choice_number=4, question=question3)
q3c4.save()

models.ChoiceVote(choice=q1c2, user=default_user).save()
models.RankVote(rank=2.0, question=question2, user=default_user).save()
models.ChoiceVote(choice=q3c1, user=default_user).save()

print(question1.get_most_popular())
print(question2.avg_rank())
print(question3.get_most_popular())
