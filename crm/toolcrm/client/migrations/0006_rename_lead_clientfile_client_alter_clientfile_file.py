# Generated by Django 4.2.7 on 2023-12-10 20:32

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("client", "0005_clientfile"),
    ]

    operations = [
        migrations.RenameField(
            model_name="clientfile",
            old_name="lead",
            new_name="client",
        ),
        migrations.AlterField(
            model_name="clientfile",
            name="file",
            field=models.FileField(upload_to="clientfiles"),
        ),
    ]