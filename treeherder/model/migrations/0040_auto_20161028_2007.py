# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('model', '0039_push_and_commit_orm'),
    ]

    operations = [
        migrations.AlterField(
            model_name='push',
            name='revision_hash',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterUniqueTogether(
            name='push',
            unique_together=set([('repository', 'revision_hash'), ('repository', 'revision')]),
        ),
    ]
