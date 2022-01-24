# Generated by Django 4.0 on 2021-12-29 01:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_rename_category_products_categorie'),
    ]

    operations = [
        migrations.CreateModel(
            name='Customers',
            fields=[
                ('_id', models.AutoField(editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('lastName', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('email', models.EmailField(blank=True, default='', max_length=254, null=True)),
                ('phone', models.CharField(blank=True, default='', max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Orders',
            fields=[
                ('_id', models.AutoField(editable=False, primary_key=True, serialize=False)),
                ('datePurchase', models.DateTimeField(blank=True, default=None, null=True)),
                ('total', models.FloatField(blank=True, default=0.0, null=True)),
                ('status', models.BooleanField(blank=True, default=True, null=True)),
                ('customer', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='base.customers')),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('_id', models.AutoField(editable=False, primary_key=True, serialize=False)),
                ('quantity', models.IntegerField(blank=True, default=0, null=True)),
                ('total', models.FloatField(blank=True, default=0.0, null=True)),
                ('order', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='base.orders')),
                ('product', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='base.products')),
            ],
        ),
        migrations.CreateModel(
            name='Donations',
            fields=[
                ('_id', models.AutoField(editable=False, primary_key=True, serialize=False)),
                ('dateDonation', models.DateTimeField(blank=True, default=None, null=True)),
                ('total', models.FloatField(blank=True, default=0.0, null=True)),
                ('optionPay', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('quantity', models.IntegerField(blank=True, default=0, null=True)),
                ('price', models.FloatField(blank=True, default=0.0, null=True)),
                ('customer', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='base.customers')),
            ],
        ),
    ]
