# Generated by Django 3.0.5 on 2020-05-12 11:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("passbook_flows", "0004_auto_20200510_2310"),
    ]

    operations = [
        migrations.AlterField(
            model_name="flow",
            name="designation",
            field=models.CharField(
                choices=[
                    ("authentication", "Authentication"),
                    ("invalidation", "Invalidation"),
                    ("enrollment", "Enrollment"),
                    ("unenrollment", "Unrenollment"),
                    ("recovery", "Recovery"),
                    ("password_change", "Password Change"),
                ],
                max_length=100,
            ),
        ),
    ]
