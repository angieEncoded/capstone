# Generated by Django 3.2.8 on 2021-12-17 15:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tabicrm', '0003_alter_customer_primary_phone'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='notes',
            field=models.TextField(blank=True, null=True),
        ),
    ]