# Generated by Django 4.2.8 on 2024-02-14 10:11

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('Student_ID', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=70)),
                ('roll', models.IntegerField()),
                ('city', models.CharField(max_length=70)),
            ],
        ),
    ]
