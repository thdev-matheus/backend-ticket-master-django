# Generated by Django 4.1.2 on 2022-10-31 18:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0002_remove_user_is_adm_alter_user_department_id"),
    ]

    operations = [
        migrations.RenameField(
            model_name="user",
            old_name="department_id",
            new_name="department",
        ),
    ]
