# Generated by Django 4.0.2 on 2022-04-18 15:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0005_transfer_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transfer',
            name='status',
            field=models.CharField(choices=[('I', 'Inserted'), ('P', 'Postponed'), ('T', 'To insert')], max_length=1, null=True),
        ),
    ]
