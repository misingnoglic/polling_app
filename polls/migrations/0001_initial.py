# Generated by Django 2.1.5 on 2019-03-17 02:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ChoiceNuanceVote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='ChoiceVote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Poll',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('published', models.BooleanField(default=False)),
                ('owner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-pk'],
            },
        ),
        migrations.CreateModel(
            name='PollTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag', models.CharField(max_length=25, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='PollUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('birthday', models.DateField(blank=True, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_number', models.PositiveSmallIntegerField()),
                ('question_text', models.CharField(max_length=100)),
            ],
            options={
                'ordering': ['poll', 'question_number'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='RankVote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rank', models.IntegerField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TextChoice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=100)),
                ('choice_number', models.PositiveSmallIntegerField()),
                ('added_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['question__poll', 'question', 'choice_number'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TextChoiceNuance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=100)),
                ('added_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('choice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.TextChoice')),
            ],
        ),
        migrations.CreateModel(
            name='RankingQuestion',
            fields=[
                ('question_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='polls.Question')),
                ('low_end', models.IntegerField()),
                ('high_end', models.IntegerField()),
            ],
            bases=('polls.question',),
        ),
        migrations.CreateModel(
            name='TextChoicesQuestion',
            fields=[
                ('question_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='polls.Question')),
                ('can_choose_multiple', models.BooleanField(default=False)),
                ('others_can_add', models.BooleanField(default=False)),
            ],
            bases=('polls.question',),
        ),
        migrations.AddField(
            model_name='question',
            name='poll',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.Poll'),
        ),
        migrations.AddField(
            model_name='poll',
            name='tags',
            field=models.ManyToManyField(to='polls.PollTag'),
        ),
        migrations.AddField(
            model_name='choicevote',
            name='choice',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.TextChoice'),
        ),
        migrations.AddField(
            model_name='choicevote',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='choicenuancevote',
            name='nuance',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.TextChoiceNuance'),
        ),
        migrations.AddField(
            model_name='choicenuancevote',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='textchoice',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.TextChoicesQuestion'),
        ),
        migrations.AddField(
            model_name='rankvote',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.RankingQuestion'),
        ),
        migrations.AlterUniqueTogether(
            name='question',
            unique_together={('question_number', 'poll'), ('question_text', 'poll')},
        ),
        migrations.AlterUniqueTogether(
            name='choicevote',
            unique_together={('choice', 'user')},
        ),
        migrations.AlterUniqueTogether(
            name='choicenuancevote',
            unique_together={('nuance', 'user')},
        ),
        migrations.AlterUniqueTogether(
            name='textchoice',
            unique_together={('question', 'text'), ('question', 'choice_number')},
        ),
        migrations.AlterUniqueTogether(
            name='rankvote',
            unique_together={('user', 'question')},
        ),
    ]
