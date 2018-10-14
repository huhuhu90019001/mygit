# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CapacityData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ip', models.CharField(max_length=64, verbose_name=b'ip')),
                ('hostdata', models.CharField(max_length=64, verbose_name=b'hostdata')),
                ('lasttime', models.DateTimeField(verbose_name='\u6700\u540e\u5de1\u68c0\u65f6\u95f4')),
                ('region', models.CharField(max_length=64, verbose_name=b'region')),
                ('module', models.CharField(max_length=64, verbose_name=b'module')),
                ('clouddomain', models.CharField(max_length=64, verbose_name=b'clouddomain')),
                ('system', models.CharField(max_length=32, verbose_name=b'system')),
            ],
            options={
                'verbose_name': '\u67e5\u8be2\u6570\u636e',
                'verbose_name_plural': '\u67e5\u8be2\u6570\u636e',
            },
        ),
    ]
