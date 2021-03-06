# Generated by Django 4.0 on 2021-12-14 20:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tabicrm', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('website', models.CharField(blank=True, max_length=255, null=True)),
                ('primary_phone', models.CharField(blank=True, max_length=255, null=True)),
                ('fax', models.CharField(blank=True, max_length=255, null=True)),
                ('secondary_phone', models.CharField(blank=True, max_length=64, null=True)),
                ('billing_address_one', models.CharField(blank=True, max_length=255, null=True)),
                ('billing_address_two', models.CharField(blank=True, max_length=255, null=True)),
                ('billing_address_city', models.CharField(blank=True, max_length=255, null=True)),
                ('billing_address_state', models.CharField(blank=True, max_length=255, null=True)),
                ('billing_address_zip', models.CharField(blank=True, max_length=255, null=True)),
                ('billing_address_country', models.CharField(blank=True, max_length=255, null=True)),
                ('shipping_address_one', models.CharField(blank=True, max_length=255, null=True)),
                ('shipping_address_two', models.CharField(blank=True, max_length=255, null=True)),
                ('shipping_address_city', models.CharField(blank=True, max_length=255, null=True)),
                ('shipping_address_state', models.CharField(blank=True, max_length=255, null=True)),
                ('shipping_address_zip', models.CharField(blank=True, max_length=255, null=True)),
                ('shipping_address_country', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
    ]
