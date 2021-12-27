# Generated by Django 4.0 on 2021-12-27 14:52

from django.db import migrations, models
import django.utils.timezone
import tabicrm.models


class Migration(migrations.Migration):

    dependencies = [
        ('tabicrm', '0014_equipment_end_of_life'),
    ]

    operations = [
        migrations.AlterField(
            model_name='equipment',
            name='end_of_life',
            field=models.DateField(default=tabicrm.models.default_three_year),
        ),
        migrations.AlterField(
            model_name='equipment',
            name='purchase_date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='equipment',
            name='warranty_end_date',
            field=models.DateField(default=tabicrm.models.default_three_year),
        ),
        migrations.AlterField(
            model_name='license',
            name='end_of_life',
            field=models.DateField(blank=True, default=tabicrm.models.default_three_year, null=True),
        ),
        migrations.AlterField(
            model_name='license',
            name='expiration_date',
            field=models.DateField(blank=True, default=tabicrm.models.default_three_year, null=True),
        ),
    ]
