# Generated by Django 5.0.7 on 2025-02-09 16:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("courses", "0010_register_model"),
    ]

    operations = [
        migrations.AddField(
            model_name="course",
            name="price",
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]
