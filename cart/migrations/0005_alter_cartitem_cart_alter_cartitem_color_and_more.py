# Generated by Django 4.2.2 on 2023-07-06 09:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("cart", "0004_cartitem_cart"),
    ]

    operations = [
        migrations.AlterField(
            model_name="cartitem",
            name="cart",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="cart.cart",
            ),
        ),
        migrations.AlterField(
            model_name="cartitem",
            name="color",
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AlterField(
            model_name="cartitem",
            name="size",
            field=models.CharField(blank=True, max_length=10),
        ),
    ]
