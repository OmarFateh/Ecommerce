# Generated by Django 2.2 on 2021-03-04 18:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0003_auto_20210225_1814'),
    ]

    operations = [
        migrations.RenameField(
            model_name='variation',
            old_name='price',
            new_name='regular_price',
        ),
    ]