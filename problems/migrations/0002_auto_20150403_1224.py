# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('problems', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='problem',
            old_name='question_text',
            new_name='problem_text',
        ),
        migrations.AddField(
            model_name='problem',
            name='problem_title',
            field=models.CharField(max_length=200, default='Test problem'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='problem',
            name='problem_value',
            field=models.IntegerField(default=5),
            preserve_default=False,
        ),
    ]
