# Generated by Django 4.0.5 on 2022-06-28 17:09

from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0002_employee'),
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('is_prospect', models.BooleanField(default=True)),
                ('company_name', models.CharField(max_length=128)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('sale_contact', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='client_salesman', to='users.employee')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            bases=('users.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Contract',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.BooleanField(default=False, verbose_name='signed')),
                ('contract_name', models.CharField(max_length=128)),
                ('contract_amount', models.FloatField()),
                ('payment_due', models.DateTimeField()),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='contract_client', to='api.client')),
                ('sale_contact', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='contract_salesman', to='users.employee')),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_status', models.CharField(choices=[('C', 'Créé'), ('E', 'En cours'), ('T', 'Terminé')], default='C', max_length=1)),
                ('attendees', models.IntegerField()),
                ('date_event', models.DateTimeField()),
                ('notes', models.CharField(blank=True, max_length=1024)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('contract', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='event_contract', to='api.contract')),
                ('support_contact', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='event_manager', to='users.employee')),
            ],
        ),
    ]
