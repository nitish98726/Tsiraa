# Generated by Django 4.2.2 on 2023-07-06 08:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("cart", "0003_alter_cartitem_color_alter_cartitem_size"),
    ]

    operations = [
        migrations.AddField(
            model_name="cartitem",
            name="cart",
            field=models.ForeignKey(
                null=True, on_delete=django.db.models.deletion.SET_NULL, to="cart.cart"
            ),
        ),
    ]
