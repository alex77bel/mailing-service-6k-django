# Generated by Django 4.2.3 on 2023-07-22 20:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailing', '0014_mailing_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mailing',
            name='clients',
            field=models.ManyToManyField(related_name='mailing', to='mailing.client', verbose_name='Клиенты'),
        ),
    ]
