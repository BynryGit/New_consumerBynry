# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('BynryConsumerModuleapp', '0001_initial'),
        ('consumerapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CourtCaseDetail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('court_remark', models.CharField(max_length=200, null=True, blank=True)),
                ('case_status', models.CharField(max_length=50, choices=[(b'Closed', b'Closed'), (b'Open', b'Open'), (b'Pending', b'Pending')])),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_on', models.DateTimeField(null=True, blank=True)),
                ('updated_by', models.CharField(max_length=50, null=True, blank=True)),
                ('created_by', models.CharField(max_length=50)),
                ('is_deleted', models.BooleanField(default=False, choices=[(True, True), (False, False)])),
            ],
        ),
        migrations.CreateModel(
            name='VigilanceDetail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('case_id', models.CharField(max_length=200, null=True)),
                ('vigilance_remark', models.CharField(max_length=200, null=True, blank=True)),
                ('vigilance_status', models.CharField(max_length=50, choices=[(b'WIP', b'WIP'), (b'Closed', b'Closed'), (b'Open', b'Open')])),
                ('vigilance_source', models.CharField(max_length=50, choices=[(b'Mobile', b'Mobile'), (b'Web', b'Web'), (b'CTI', b'CTI')])),
                ('registered_date', models.DateTimeField(null=True, blank=True)),
                ('theft_found', models.CharField(max_length=50, choices=[(b'Yes', b'Yes'), (b'No', b'No')])),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_on', models.DateTimeField(null=True, blank=True)),
                ('updated_by', models.CharField(max_length=50, null=True, blank=True)),
                ('created_by', models.CharField(max_length=50)),
                ('is_deleted', models.BooleanField(default=False, choices=[(True, True), (False, False)])),
                ('bill_cycle', models.ForeignKey(blank=True, to='BynryConsumerModuleapp.BillCycle', null=True)),
                ('consumer_id', models.ForeignKey(to='consumerapp.ConsumerDetails', null=True)),
                ('route', models.ForeignKey(blank=True, to='BynryConsumerModuleapp.RouteDetail', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='VigilancePenalyDetail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('payment', models.CharField(max_length=200, null=True, blank=True)),
                ('payment_status', models.CharField(max_length=50, choices=[(b'Closed', b'Closed'), (b'Open', b'Open')])),
                ('payment_method', models.CharField(max_length=50, choices=[(b'Online', b'Online'), (b'Cash', b'Cash'), (b'Cheque', b'Cheque')])),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_on', models.DateTimeField(null=True, blank=True)),
                ('updated_by', models.CharField(max_length=50, null=True, blank=True)),
                ('created_by', models.CharField(max_length=50)),
                ('is_deleted', models.BooleanField(default=False, choices=[(True, True), (False, False)])),
                ('vigilance_id', models.ForeignKey(to='vigilanceapp.VigilanceDetail', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='VigilanceType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('vigilance_type', models.CharField(max_length=500, null=True, blank=True)),
                ('vigilance_code', models.CharField(max_length=100, null=True, blank=True)),
                ('updated_by', models.CharField(max_length=50, null=True, blank=True)),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_on', models.DateField(null=True, blank=True)),
                ('created_by', models.CharField(max_length=50)),
                ('is_deleted', models.BooleanField(default=False, choices=[(True, True), (False, False)])),
            ],
        ),
        migrations.AddField(
            model_name='vigilancedetail',
            name='vigilance_type_id',
            field=models.ForeignKey(to='vigilanceapp.VigilanceType', null=True),
        ),
        migrations.AddField(
            model_name='vigilancedetail',
            name='zone',
            field=models.ForeignKey(to='BynryConsumerModuleapp.Zone', null=True),
        ),
        migrations.AddField(
            model_name='courtcasedetail',
            name='vigilance_id',
            field=models.ForeignKey(to='vigilanceapp.VigilanceDetail', null=True),
        ),
    ]
