# Generated by Django 4.0 on 2021-12-21 12:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tabicrm', '0008_remove_license_type_remove_license_vendor_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='license',
            old_name='expiriration_date',
            new_name='expiration_date',
        ),
    ]