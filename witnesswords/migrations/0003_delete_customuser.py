# Generated by Django 5.1.1 on 2024-09-16 10:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("witnesswords", "0002_customuser"),
    ]

    operations = [
        migrations.DeleteModel(
            name="CustomUser",
        ),
    ]
