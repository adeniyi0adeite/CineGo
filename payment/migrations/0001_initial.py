# Generated by Django 5.1.4 on 2025-01-04 17:23

import django.utils.timezone
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('reference', models.CharField(default=uuid.uuid4, max_length=100, unique=True)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('completed', 'Completed'), ('failed', 'Failed')], default='pending', max_length=20)),
                ('payment_type', models.CharField(choices=[('subscription', 'Subscription'), ('pay_per_watch', 'Pay Per Watch')], max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='SubscriptionPayment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateTimeField(auto_now_add=True)),
                ('end_date', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='SubscriptionPlan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('Basic', 'Basic'), ('Premium', 'Premium'), ('Vip', 'VIP')], max_length=100, unique=True)),
                ('price', models.DecimalField(decimal_places=2, default=1000.0, max_digits=6)),
                ('duration', models.IntegerField(default=30, help_text='Duration of the plan in days')),
                ('resolution', models.CharField(choices=[('HD', 'HD'), ('Full HD', 'Full HD'), ('4K', '4K')], default='HD', max_length=50)),
                ('device', models.CharField(blank=True, max_length=100, null=True)),
                ('support', models.CharField(choices=[('Limited Support', 'Limited Support'), ('24/7 Support', '24/7 Support')], default='Limited Support', max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='VideoAccessPayment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('transaction_reference', models.CharField(max_length=100, unique=True)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('successful', 'Successful')], default='pending', max_length=20)),
                ('date_paid', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
    ]
