# Generated by Django 4.2.6 on 2023-12-14 12:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_remove_likequestion_unique_like_question_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='likequestion',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='like_q', to='app.question'),
        ),
    ]
