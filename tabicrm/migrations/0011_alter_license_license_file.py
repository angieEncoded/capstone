# Generated by Django 4.0 on 2021-12-21 20:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tabicrm', '0010_license_license_file_license_license_key_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='license',
            name='license_file',
            field=models.FileField(blank=True, null=True, upload_to='licenses/% m/% d/% Y/'),
        ),
    ]
