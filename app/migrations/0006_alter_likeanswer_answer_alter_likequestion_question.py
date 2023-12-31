# Generated by Django 4.2.6 on 2023-12-14 12:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_alter_likeanswer_answer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='likeanswer',
            name='answer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='like_model', to='app.answer'),
        ),
        migrations.AlterField(
            model_name='likequestion',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='like_model', to='app.question'),
        ),
    ]
