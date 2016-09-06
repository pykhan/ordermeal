# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-05 14:47
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import localflavor.us.models
import web.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Category Name')),
            ],
            options={
                'verbose_name_plural': 'Categories',
                'verbose_name': 'Category',
            },
            bases=(web.models.ModelSaveMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Child',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=30, verbose_name='First Name')),
                ('middle_name', models.CharField(blank=True, max_length=30, null=True, verbose_name='Middle Name')),
                ('last_name', models.CharField(max_length=30, verbose_name='Last Name')),
                ('birth_date', models.DateField(blank=True, null=True, verbose_name='Birth Date')),
                ('allergies', models.TextField(blank=True, null=True, verbose_name='Allergies')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Parent')),
            ],
            options={
                'verbose_name_plural': 'Children',
                'verbose_name': 'Child',
            },
            bases=(web.models.ModelSaveMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(blank=True, max_length=30, null=True, verbose_name='First Name')),
                ('middle_name', models.CharField(blank=True, max_length=30, null=True, verbose_name='Middle Name')),
                ('last_name', models.CharField(blank=True, max_length=30, null=True, verbose_name='Last Name')),
                ('work_phone', localflavor.us.models.PhoneNumberField(blank=True, null=True, verbose_name='Work Phone')),
                ('cell_phone', localflavor.us.models.PhoneNumberField(blank=True, null=True, verbose_name='Cell Phone')),
                ('address_1', models.CharField(blank=True, max_length=100, null=True, verbose_name='Address 1')),
                ('address_2', models.CharField(blank=True, max_length=100, null=True, verbose_name='Address 2')),
                ('city', models.CharField(blank=True, max_length=100, null=True, verbose_name='City')),
                ('state', models.CharField(blank=True, choices=[('AL', 'Alabama'), ('AK', 'Alaska'), ('AS', 'American Samoa'), ('AZ', 'Arizona'), ('AR', 'Arkansas'), ('AA', 'Armed Forces Americas'), ('AE', 'Armed Forces Europe'), ('AP', 'Armed Forces Pacific'), ('CA', 'California'), ('CO', 'Colorado'), ('CT', 'Connecticut'), ('DE', 'Delaware'), ('DC', 'District of Columbia'), ('FL', 'Florida'), ('GA', 'Georgia'), ('GU', 'Guam'), ('HI', 'Hawaii'), ('ID', 'Idaho'), ('IL', 'Illinois'), ('IN', 'Indiana'), ('IA', 'Iowa'), ('KS', 'Kansas'), ('KY', 'Kentucky'), ('LA', 'Louisiana'), ('ME', 'Maine'), ('MD', 'Maryland'), ('MA', 'Massachusetts'), ('MI', 'Michigan'), ('MN', 'Minnesota'), ('MS', 'Mississippi'), ('MO', 'Missouri'), ('MT', 'Montana'), ('NE', 'Nebraska'), ('NV', 'Nevada'), ('NH', 'New Hampshire'), ('NJ', 'New Jersey'), ('NM', 'New Mexico'), ('NY', 'New York'), ('NC', 'North Carolina'), ('ND', 'North Dakota'), ('MP', 'Northern Mariana Islands'), ('OH', 'Ohio'), ('OK', 'Oklahoma'), ('OR', 'Oregon'), ('PA', 'Pennsylvania'), ('PR', 'Puerto Rico'), ('RI', 'Rhode Island'), ('SC', 'South Carolina'), ('SD', 'South Dakota'), ('TN', 'Tennessee'), ('TX', 'Texas'), ('UT', 'Utah'), ('VT', 'Vermont'), ('VI', 'Virgin Islands'), ('VA', 'Virginia'), ('WA', 'Washington'), ('WV', 'West Virginia'), ('WI', 'Wisconsin'), ('WY', 'Wyoming')], default='NJ', max_length=2, null=True)),
                ('zip_code', models.CharField(blank=True, max_length=5, null=True)),
                ('child', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.Child', verbose_name='Child')),
            ],
            options={
                'verbose_name_plural': 'Doctors',
                'verbose_name': 'Doctor',
            },
            bases=(web.models.ModelSaveMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Ingredient')),
            ],
            options={
                'verbose_name_plural': 'Ingredients',
                'verbose_name': 'Ingredient',
            },
            bases=(web.models.ModelSaveMixin, models.Model),
        ),
        migrations.CreateModel(
            name='ParentProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cell_phone', localflavor.us.models.PhoneNumberField(verbose_name='Cell Phone')),
                ('home_phone', localflavor.us.models.PhoneNumberField(blank=True, null=True, verbose_name='Home Phone')),
                ('work_phone', localflavor.us.models.PhoneNumberField(blank=True, null=True, verbose_name='Work Phone')),
                ('address_1', models.CharField(max_length=100, verbose_name='Address 1')),
                ('address_2', models.CharField(blank=True, max_length=100, null=True, verbose_name='Address 2')),
                ('city', models.CharField(max_length=100, verbose_name='City')),
                ('state', models.CharField(choices=[('AL', 'Alabama'), ('AK', 'Alaska'), ('AS', 'American Samoa'), ('AZ', 'Arizona'), ('AR', 'Arkansas'), ('AA', 'Armed Forces Americas'), ('AE', 'Armed Forces Europe'), ('AP', 'Armed Forces Pacific'), ('CA', 'California'), ('CO', 'Colorado'), ('CT', 'Connecticut'), ('DE', 'Delaware'), ('DC', 'District of Columbia'), ('FL', 'Florida'), ('GA', 'Georgia'), ('GU', 'Guam'), ('HI', 'Hawaii'), ('ID', 'Idaho'), ('IL', 'Illinois'), ('IN', 'Indiana'), ('IA', 'Iowa'), ('KS', 'Kansas'), ('KY', 'Kentucky'), ('LA', 'Louisiana'), ('ME', 'Maine'), ('MD', 'Maryland'), ('MA', 'Massachusetts'), ('MI', 'Michigan'), ('MN', 'Minnesota'), ('MS', 'Mississippi'), ('MO', 'Missouri'), ('MT', 'Montana'), ('NE', 'Nebraska'), ('NV', 'Nevada'), ('NH', 'New Hampshire'), ('NJ', 'New Jersey'), ('NM', 'New Mexico'), ('NY', 'New York'), ('NC', 'North Carolina'), ('ND', 'North Dakota'), ('MP', 'Northern Mariana Islands'), ('OH', 'Ohio'), ('OK', 'Oklahoma'), ('OR', 'Oregon'), ('PA', 'Pennsylvania'), ('PR', 'Puerto Rico'), ('RI', 'Rhode Island'), ('SC', 'South Carolina'), ('SD', 'South Dakota'), ('TN', 'Tennessee'), ('TX', 'Texas'), ('UT', 'Utah'), ('VT', 'Vermont'), ('VI', 'Virgin Islands'), ('VA', 'Virginia'), ('WA', 'Washington'), ('WV', 'West Virginia'), ('WI', 'Wisconsin'), ('WY', 'Wyoming')], default='NJ', max_length=2)),
                ('zip_code', models.CharField(blank=True, max_length=5, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name="Parent's Name")),
            ],
            options={
                'verbose_name_plural': 'Parent Profiles',
                'verbose_name': 'Parent Profile',
            },
            bases=(web.models.ModelSaveMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('unit_price', models.DecimalField(decimal_places=2, max_digits=5)),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('expires_at', models.DateField(blank=True, null=True, verbose_name='Expires At')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.Category')),
                ('ingredient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.Ingredient', verbose_name='Ingredient')),
            ],
            options={
                'verbose_name_plural': 'Products',
                'verbose_name': 'Product',
            },
            bases=(web.models.ModelSaveMixin, models.Model),
        ),
    ]
