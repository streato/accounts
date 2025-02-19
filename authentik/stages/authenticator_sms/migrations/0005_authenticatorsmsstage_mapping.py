# Generated by Django 4.1.2 on 2022-10-13 20:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("authentik_events", "0002_alter_notificationtransport_mode"),
        ("authentik_stages_authenticator_sms", "0004_authenticatorsmsstage_verify_only_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="authenticatorsmsstage",
            name="mapping",
            field=models.ForeignKey(
                default=None,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="authentik_events.notificationwebhookmapping",
                help_text="Optionally modify the payload being sent to custom providers.",
            ),
        ),
    ]
