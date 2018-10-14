# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homework', '0002_auto_20181005_1216'),
    ]

    operations = [
        migrations.CreateModel(
            name='CapacityData2',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ip', models.CharField(max_length=64, null=True, verbose_name=b'ip', blank=True)),
                ('mem', models.CharField(max_length=64, verbose_name=b'mem')),
                ('disk', models.CharField(max_length=64, verbose_name=b'disk')),
                ('cpu', models.CharField(max_length=64, verbose_name=b'cpu')),
                ('createtime', models.DateTimeField(verbose_name='\u4fdd\u5b58\u65f6\u95f4')),
            ],
            options={
                'verbose_name': '\u78c1\u76d8\u5bb9\u91cf\u6570\u636e',
                'verbose_name_plural': '\u78c1\u76d8\u5bb9\u91cf\u6570\u636e',
            },
        ),
        migrations.CreateModel(
            name='CapacityData3',
            fields=[
                ('index', models.AutoField(max_length=64, serialize=False, verbose_name=b'index', primary_key=True)),
                ('ip', models.CharField(max_length=64, null=True, verbose_name=b'ip', blank=True)),
                ('mem_disk_cpu', models.CharField(max_length=64, verbose_name=b'mem_disk_cpu')),
                ('exec_time', models.CharField(max_length=64, verbose_name=b'exec_time')),
                ('set', models.CharField(max_length=64, verbose_name=b'set')),
                ('module', models.CharField(max_length=64, verbose_name=b'module')),
                ('instname', models.CharField(max_length=64, verbose_name=b'instname')),
                ('osname', models.CharField(max_length=64, verbose_name=b'osname')),
            ],
            options={
                'verbose_name': '\u78c1\u76d8\u5bb9\u91cf\u6570\u636e',
                'verbose_name_plural': '\u78c1\u76d8\u5bb9\u91cf\u6570\u636e',
            },
        ),
        migrations.CreateModel(
            name='OperateData',
            fields=[
                ('index', models.AutoField(max_length=64, serialize=False, verbose_name=b'index', primary_key=True)),
                ('ip', models.CharField(max_length=64, null=True, verbose_name=b'ip', blank=True)),
                ('operator', models.CharField(max_length=64, verbose_name=b'operator')),
                ('exec_time', models.CharField(max_length=64, verbose_name=b'exec_time')),
                ('operate_style', models.CharField(max_length=64, verbose_name=b'operate_style')),
            ],
            options={
                'ordering': ['-index'],
                'verbose_name': '\u64cd\u4f5c\u8bb0\u5f55\u6570\u636e',
                'verbose_name_plural': '\u64cd\u4f5c\u8bb0\u5f55\u6570\u636e',
            },
        ),
        migrations.CreateModel(
            name='TaskLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('operator', models.CharField(max_length=64, verbose_name='\u64cd\u4f5c\u4eba')),
                ('starttime', models.DateTimeField(verbose_name='\u8d77\u59cb\u6267\u884c\u65f6\u95f4')),
                ('endtime', models.DateTimeField(verbose_name='\u7ed3\u675f\u6267\u884c\u65f6\u95f4')),
                ('log', models.TextField(null=True, verbose_name='\u6267\u884c\u65e5\u5fd7', blank=True)),
                ('ip', models.IPAddressField(verbose_name='\u6267\u884cIP')),
                ('result', models.CharField(max_length=64, verbose_name='\u6267\u884c\u7ed3\u679c')),
                ('stepname', models.CharField(max_length=64, verbose_name='\u6b65\u9aa4\u540d')),
            ],
            options={
                'verbose_name': '\u6267\u884c\u5386\u53f2\u65e5\u5fd7',
                'verbose_name_plural': '\u6267\u884c\u5386\u53f2\u65e5\u5fd7',
            },
        ),
        migrations.CreateModel(
            name='TaskResult',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('func', models.CharField(max_length=64, verbose_name='\u6267\u884c\u51fd\u6570')),
                ('result', models.TextField(max_length=64, verbose_name='\u51fd\u6570\u8fd4\u56de\u7ed3\u679c')),
            ],
            options={
                'verbose_name': '\u4efb\u52a1\u6267\u884c\u7ed3\u679c',
                'verbose_name_plural': '\u4efb\u52a1\u6267\u884c\u7ed3\u679c',
            },
        ),
        migrations.DeleteModel(
            name='HostData',
        ),
    ]
