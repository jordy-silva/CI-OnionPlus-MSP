# -*- coding: utf-8 -*-
# Generated by Django 1.11.28 on 2020-02-15 12:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ticket_type', models.CharField(choices=[('BUG', 'Bug'), ('FEATURE', 'Feature')], default='FEATURE', max_length=7)),
                ('user_id', models.CharField(max_length=254)),
                ('subject', models.CharField(max_length=254)),
                ('description', models.TextField()),
                ('creation_ts', models.DateTimeField(auto_now_add=True)),
                ('number_votes', models.IntegerField()),
                ('status', models.CharField(choices=[('TODO', 'To Do'), ('DOING', 'Doing'), ('DONE', 'Done')], default='TODO', max_length=5)),
            ],
        ),
    ]
