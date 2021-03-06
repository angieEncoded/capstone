# Generated by Django 4.0 on 2021-12-21 13:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tabicrm', '0009_rename_expiriration_date_license_expiration_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='license',
            name='license_file',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='license',
            name='license_key',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='license',
            name='purchase_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
