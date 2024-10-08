# Generated by Django 5.1.1 on 2024-09-18 08:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("witnesswords", "0003_delete_customuser"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="status",
            field=models.CharField(
                choices=[("completed", "Completed"), ("in_progress", "In Progress")],
                default="in_progress",
                max_length=50,
            ),
        ),
    ]
