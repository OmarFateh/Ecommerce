# Generated by Django 2.2 on 2021-04-05 23:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0001_initial'),
        ('order', '0004_order_delivery_option'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='payment_method',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='orders', to='checkout.PaymentMethod'),
        ),
        migrations.AlterField(
            model_name='order',
            name='delivery_option',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='orders', to='checkout.DeliveryOption'),
        ),
    ]