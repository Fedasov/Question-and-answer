# Generated by Django 4.2.6 on 2023-12-14 11:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_likequestion_unique_like_question'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='likequestion',
            name='unique_like_question',
        ),
        migrations.AlterUniqueTogether(
            name='likeanswer',
            unique_together={('user', 'answer')},
        ),
        migrations.AlterUniqueTogether(
            name='likequestion',
            unique_together={('user', 'question')},
        ),
    ]