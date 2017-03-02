# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.contrib.auth.models
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='Area',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('area_name', models.CharField(max_length=250)),
                ('created_by', models.CharField(max_length=50)),
                ('updated_by', models.CharField(max_length=50, null=True, blank=True)),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_on', models.DateTimeField(null=True, blank=True)),
                ('is_deleted', models.BooleanField(default=False, choices=[(True, True), (False, False)])),
            ],
        ),
        migrations.CreateModel(
            name='BillCycle',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('bill_cycle_code', models.CharField(max_length=100)),
                ('bill_cycle_name', models.CharField(max_length=100, null=True)),
                ('created_by', models.CharField(max_length=50)),
                ('updated_by', models.CharField(max_length=50, null=True, blank=True)),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_on', models.DateTimeField(null=True, blank=True)),
                ('is_deleted', models.BooleanField(default=False, choices=[(True, True), (False, False)])),
                ('area', models.ForeignKey(blank=True, to='BynryConsumerModuleapp.Area', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='BillingUnit',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('B_U', models.CharField(max_length=20, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('city', models.CharField(default=None, max_length=500)),
                ('created_by', models.CharField(max_length=50)),
                ('updated_by', models.CharField(max_length=50, null=True, blank=True)),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_on', models.DateTimeField(null=True, blank=True)),
                ('is_deleted', models.BooleanField(default=False, choices=[(True, True), (False, False)])),
            ],
        ),
        migrations.CreateModel(
            name='ProcessingCycle',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('P_C', models.CharField(max_length=20, null=True)),
                ('B_U', models.ForeignKey(to='BynryConsumerModuleapp.BillingUnit', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='RouteDetail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('route_code', models.CharField(max_length=500)),
                ('created_by', models.CharField(max_length=50)),
                ('updated_by', models.CharField(max_length=50, null=True, blank=True)),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_on', models.DateTimeField(null=True, blank=True)),
                ('is_deleted', models.BooleanField(default=False, choices=[(True, True), (False, False)])),
                ('billcycle', models.ForeignKey(blank=True, to='BynryConsumerModuleapp.BillCycle', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='State',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('state', models.CharField(max_length=500, blank=True)),
                ('created_by', models.CharField(max_length=50)),
                ('updated_by', models.CharField(max_length=50, null=True, blank=True)),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_on', models.DateTimeField(null=True, blank=True)),
                ('is_deleted', models.BooleanField(default=False, choices=[(True, True), (False, False)])),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('user_ptr', models.OneToOneField(parent_link=True, auto_created=True, to=settings.AUTH_USER_MODEL)),
                ('user_id', models.AutoField(serialize=False, editable=False, primary_key=True)),
                ('user_name', models.CharField(default=None, max_length=100, null=True, blank=True)),
            ],
            options={
                'abstract': False,
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='UserPrivilege',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('privilege', models.CharField(max_length=500)),
                ('created_by', models.CharField(max_length=50)),
                ('updated_by', models.CharField(max_length=50, null=True, blank=True)),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_on', models.DateTimeField(null=True, blank=True)),
                ('is_deleted', models.BooleanField(default=False, choices=[(True, True), (False, False)])),
                ('parent', models.ForeignKey(blank=True, to='BynryConsumerModuleapp.UserPrivilege', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserRole',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('role', models.CharField(max_length=500)),
                ('description', models.CharField(max_length=500, null=True, blank=True)),
                ('status', models.CharField(default=b'Active', max_length=20, choices=[(b'Active', b'Active'), (b'Inactive', b'Inactive')])),
                ('created_by', models.CharField(max_length=50)),
                ('updated_by', models.CharField(max_length=50, null=True, blank=True)),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_on', models.DateTimeField(null=True, blank=True)),
                ('is_deleted', models.BooleanField(default=False, choices=[(True, True), (False, False)])),
                ('privilege', models.ManyToManyField(to='BynryConsumerModuleapp.UserPrivilege')),
            ],
        ),
        migrations.CreateModel(
            name='Utility',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('utility', models.CharField(max_length=100)),
                ('created_by', models.CharField(max_length=50)),
                ('updated_by', models.CharField(max_length=50, null=True, blank=True)),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_on', models.DateTimeField(null=True, blank=True)),
                ('is_deleted', models.BooleanField(default=False, choices=[(True, True), (False, False)])),
            ],
        ),
        migrations.CreateModel(
            name='Zone',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('zone_name', models.CharField(max_length=250)),
                ('created_by', models.CharField(max_length=50)),
                ('updated_by', models.CharField(max_length=50, null=True, blank=True)),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_on', models.DateTimeField(null=True, blank=True)),
                ('is_deleted', models.BooleanField(default=False, choices=[(True, True), (False, False)])),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('contact_no', models.CharField(max_length=15)),
                ('address_line_1', models.CharField(max_length=500, blank=True)),
                ('address_line_2', models.CharField(max_length=500, blank=True)),
                ('pincode', models.CharField(max_length=500, blank=True)),
                ('employee_id', models.CharField(max_length=100, blank=True)),
                ('status', models.CharField(default=b'Active', max_length=20, choices=[(b'Active', b'Active'), (b'Inactive', b'Inactive')])),
                ('created_by', models.CharField(max_length=500)),
                ('updated_by', models.CharField(max_length=500, null=True, blank=True)),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_on', models.DateTimeField(null=True, blank=True)),
                ('is_deleted', models.BooleanField(default=False, choices=[(True, True), (False, False)])),
            ],
            options={
                'abstract': False,
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            bases=('BynryConsumerModuleapp.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.AddField(
            model_name='city',
            name='state',
            field=models.ForeignKey(blank=True, to='BynryConsumerModuleapp.State', null=True),
        ),
        migrations.AddField(
            model_name='billingunit',
            name='city',
            field=models.ForeignKey(blank=True, to='BynryConsumerModuleapp.City', null=True),
        ),
        migrations.AddField(
            model_name='billcycle',
            name='city',
            field=models.ForeignKey(blank=True, to='BynryConsumerModuleapp.City', null=True),
        ),
        migrations.AddField(
            model_name='billcycle',
            name='utility',
            field=models.ForeignKey(blank=True, to='BynryConsumerModuleapp.Utility', null=True),
        ),
        migrations.AddField(
            model_name='billcycle',
            name='zone',
            field=models.ForeignKey(blank=True, to='BynryConsumerModuleapp.Zone', null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='city',
            field=models.ForeignKey(to='BynryConsumerModuleapp.City', null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='role',
            field=models.ForeignKey(blank=True, to='BynryConsumerModuleapp.UserRole', null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='state',
            field=models.ForeignKey(to='BynryConsumerModuleapp.State', null=True),
        ),
    ]
