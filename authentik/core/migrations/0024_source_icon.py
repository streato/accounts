# Generated by Django 4.1.3 on 2022-11-15 20:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("authentik_core", "0023_source_authentik_c_slug_ccb2e5_idx_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="source",
            name="icon",
            field=models.FileField(
                default=None, max_length=500, null=True, upload_to="source-icons/"
            ),
        ),
    ]
