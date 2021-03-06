# Generated by Django 3.1.1 on 2020-09-05 01:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('user_id', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('user_name', models.CharField(max_length=50)),
                ('user_psw', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Session',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.CharField(max_length=100)),
                ('course_id', models.CharField(max_length=40)),
                ('category', models.CharField(max_length=5)),
                ('session_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recommender.user')),
            ],
        ),
    ]
