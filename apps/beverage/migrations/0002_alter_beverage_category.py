# Generated by Django 4.2 on 2024-04-29 15:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("beverage", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="beverage",
            name="category",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="beverages",
                to="beverage.category",
            ),
        ),
    ]
