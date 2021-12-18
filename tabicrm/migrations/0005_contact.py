# Generated by Django 4.0 on 2021-12-18 14:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tabicrm', '0004_customer_notes'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('job_title', models.CharField(max_length=255)),
                ('extension', models.CharField(max_length=255)),
                ('notes', models.TextField(blank=True, null=True)),
                ('assigned_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contact_customer', to='tabicrm.customer')),
            ],
        ),
    ]
