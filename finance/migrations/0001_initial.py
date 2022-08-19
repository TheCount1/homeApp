# Generated by Django 4.0.2 on 2022-02-20 06:44

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('number', models.CharField(max_length=255)),
                ('owner', models.CharField(choices=[('A', 'Adrian'), ('J', 'Asia')], max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='AssetType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='FinancialChange',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('amount_gr', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('date', models.DateField()),
                ('direction', models.CharField(choices=[('I', 'Incoming'), ('O', 'Outgoing')], max_length=1)),
                ('account', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='finance.account')),
                ('asset_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='finance.assettype')),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='finance.category')),
            ],
        ),
        migrations.CreateModel(
            name='Transfer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sender_receiver', models.CharField(max_length=255)),
                ('title', models.CharField(max_length=255)),
                ('outer_account', models.CharField(max_length=30)),
                ('date', models.DateField()),
                ('amount_gr', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('direction', models.CharField(choices=[('I', 'Incoming'), ('O', 'Outgoing')], max_length=1)),
                ('financial_change', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='finance.financialchange')),
                ('inner_account', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='finance.account')),
            ],
        ),
        migrations.CreateModel(
            name='Reduction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('B', 'Between Accounts'), ('R', 'Loan Return'), ('K', 'Brokerage')], max_length=1)),
                ('reduced', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reduced', to='finance.financialchange')),
                ('reductor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reductor', to='finance.financialchange')),
            ],
        ),
    ]
