# Generated by Django 4.0 on 2021-12-27 20:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tabicrm', '0017_contact_created_on_contact_updated_by_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255)),
                ('status', models.CharField(choices=[('OPEN', 'OPEN'), ('IN_PROGRESS', 'IN PROGRESS'), ('WAITING_ON_CUSTOMER', 'WAITING ON CUSTOMER'), ('CLOSED', 'CLOSED')], default='OPEN', max_length=255)),
                ('priority', models.CharField(choices=[('LOW', 'LOW'), ('NORMAL', 'NORMAL'), ('HIGH', 'HIGH'), ('URGENT', 'URGENT')], default='NORMAL', max_length=255)),
                ('results', models.CharField(choices=[('SOLVED_ON_PHONE', 'SOLVED_ON_PHONE'), ('SERVER_SERVICE', 'SERVER_SERVICE'), ('ROUTER_SERVICE', 'ROUTER_SERVICE'), ('CONTRACT_SERVICE', 'CONTRACT_SERVICE'), ('NON_CONTRACT_SERVICE', 'NON_CONTRACT_SERVICE')], default='SOLVED_ON_PHONE', max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('solution', models.TextField(blank=True, null=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('added_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='ticket_addedby', to='tabicrm.user')),
                ('assigned_to', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='ticket_assignedto', to='tabicrm.user')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='customer_ticket', to='tabicrm.customer')),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='ticket_updatedon', to='tabicrm.user')),
            ],
        ),
    ]
