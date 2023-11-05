# Generated by Django 4.2.1 on 2023-08-07 10:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecom_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Create_Card',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('card_number', models.IntegerField()),
                ('exp_year', models.CharField(max_length=30)),
                ('exp_month', models.CharField(max_length=30)),
                ('CSV', models.IntegerField()),
            ],
        ),
        migrations.AddField(
            model_name='checkoutcart',
            name='is_completed',
            field=models.BooleanField(default=False),
        ),
    ]